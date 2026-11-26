// Culture Kanban – simulation engine. Pure functions, no DOM.
// Works in the browser (window.CK) and in node (module.exports).
(function (root) {
  'use strict';

  var DECK = { smooth: 18, breakthrough: 2, dependency: 3, longer: 3, rework: 2, urgent: 2, external: 2 };
  var CARD_TEXT = {
    smooth: 'Smooth hour – move the chosen task one step.',
    breakthrough: 'Breakthrough – finish the chosen task, or lift an external block.',
    dependency: 'Dependency – the chosen task turns out to need another task first.',
    longer: 'Takes longer – the hour goes into the chosen task, but it does not move.',
    rework: 'Rework – someone wants changes: a started task goes back to Not Started.',
    urgent: 'Urgent request – a new task lands in Not Started. The hour goes to handling it.',
    external: 'External block – the chosen task waits for someone outside the team.'
  };
  // Cards that planning finds in advance (they become smooth hours), and how many of each are left.
  var PLANNED_AWAY = { dependency: true, longer: true };

  function rng(seed) { // mulberry32
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function shuffledDeck(seed, deck) {
    var r = rng(seed), d = [];
    Object.keys(deck).forEach(function (k) { for (var i = 0; i < deck[k]; i++) d.push(k); });
    for (var i = d.length - 1; i > 0; i--) {
      var j = Math.floor(r() * (i + 1)), t = d[i]; d[i] = d[j]; d[j] = t;
    }
    return d;
  }

  // col: 'ns' Not Started, 'bl' Blocked (external), 'ip' In Progress, 'done'
  function newState(nTasks) {
    var cards = [];
    for (var i = 0; i < nTasks; i++) cards.push(newCard(i + 1));
    return { cards: cards, turn: 0, idle: 0, collab: 0, log: [] };
  }

  function newCard(id) {
    return { id: id, col: 'ns', dep: null, owner: null, hours: 0, rework: false, urgent: false };
  }

  function byId(s, id) { return s.cards[id - 1]; }
  function depActive(s, c) { return c.dep !== null && byId(s, c.dep).col !== 'done'; }

  // A task that an unfinished task is waiting for is a "helper":
  // it may always be started and does not count against the WIP limit.
  function isHelper(s, c) {
    if (c.col === 'done') return false;
    return s.cards.some(function (o) { return o.col !== 'done' && o.dep === c.id; });
  }

  function wipCount(s, opt) {
    return s.cards.filter(function (c) {
      var inWip = c.col === 'ip' || (opt.blockedCountsWip && c.col === 'bl');
      return inWip && !isHelper(s, c);
    }).length;
  }

  function candidates(s, opt) {
    var room = opt.wip === null || wipCount(s, opt) < opt.wip;
    return s.cards.filter(function (c) {
      if (c.col === 'done' || depActive(s, c)) return false;
      if (c.col === 'bl') return opt.chaseBlocked;
      if (c.col === 'ns') return room || isHelper(s, c);
      return true;
    });
  }

  function reaches(s, fromId, targetId) { // does fromId's dependency chain reach targetId?
    var seen = {}, cur = fromId;
    while (cur !== null && !seen[cur]) {
      if (cur === targetId) return true;
      seen[cur] = true;
      cur = byId(s, cur).dep;
    }
    return false;
  }

  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }

  // How willing players are to work on a task someone else started.
  // low: only when there is nothing else to do.
  var OTHERS_WEIGHT = { high: 1, medium: 0.35, low: 0 };

  function pickWeighted(r, arr, weights) {
    var x = r() * weights.reduce(function (a, b) { return a + b; }, 0);
    for (var i = 0; i < arr.length; i++) { x -= weights[i]; if (x < 0) return arr[i]; }
    return arr[arr.length - 1];
  }

  function pickTask(s, r, cand, player, opt) {
    // Round 2 (pull): look upstream from Done. 1) finish something in In Progress,
    // 2) resolve a dependency, 3) chase an external block, 4) only then start a new task.
    // Willingness to collaborate decides whose tasks count: with low willingness a player
    // walks the order over their own tasks (and new ones) first, other people's only as a last resort.
    if (opt.pull) {
      var tiers = [
        function (c) { return c.col === 'ip'; },
        function (c) { return isHelper(s, c); },
        function (c) { return c.col === 'bl'; },
        function (c) { return c.col === 'ns'; }
      ];
      var ow2 = OTHERS_WEIGHT[opt.collab];
      var mine = function (c) { return c.col === 'ns' || c.owner === player; };
      var passes = ow2 === 0 ? [mine, function () { return true; }] : [function () { return true; }];
      for (var q = 0; q < passes.length; q++) {
        for (var k = 0; k < tiers.length; k++) {
          var tier = cand.filter(tiers[k]).filter(passes[q]);
          if (tier.length) return pickWeighted(r, tier, tier.map(function (c) { return mine(c) || !ow2 ? 1 : ow2; }));
        }
      }
    }
    // People want to finish what they started: an own task that can move beats starting something new.
    var own = cand.filter(function (c) { return c.col === 'ip' && c.owner === player; });
    if (own.length) return pick(r, own);
    var fresh = cand.filter(function (c) { return c.col === 'ns'; });
    var going = cand.filter(function (c) { return c.col !== 'ns'; });
    var ow = OTHERS_WEIGHT[opt.collab];
    var gw = going.map(function (c) { return c.owner === player ? 1 : ow; });
    var goingOk = gw.some(function (w) { return w > 0; });
    if (fresh.length && goingOk) {
      // Without kanban habits players would rather start something new (pNew of the time).
      return r() < opt.pNew ? pick(r, fresh) : pickWeighted(r, going, gw);
    }
    if (fresh.length) return pick(r, fresh);
    if (goingOk) return pickWeighted(r, going, gw);
    return pick(r, going); // emergency: only other people's tasks are left
  }

  // A planning turn: the player maps the tasks with the team instead of drawing a card.
  function planTurn(s, player) {
    s.turn++;
    var e = { turn: s.turn, player: player, draw: null, chosen: null,
      action: 'Plans with the team – maps which tasks depend on which (no card drawn).' };
    s.log.push(e); return e;
  }

  // Planning finds most dependencies and underestimated tasks before work starts.
  // Of each such card type only keepShare is left; the rest become smooth hours.
  function plannedDeck(deck, seed, keepShare) {
    var r = rng(seed * 31 + 7), out = deck.slice(), planned = {};
    Object.keys(PLANNED_AWAY).forEach(function (type) {
      var idx = [];
      deck.forEach(function (d, i) { if (d === type) idx.push(i); });
      for (var i = idx.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
      idx.slice(Math.round(idx.length * keepShare)).forEach(function (i) { out[i] = 'smooth'; planned[i] = type; });
    });
    return { deck: out, planned: planned };
  }

  // Cards that hit the team whatever task was chosen. Return a description, or null if not such a card.
  function teamEvent(s, draw, chosen, r) {
    if (draw === 'urgent') {
      var n = newCard(s.cards.length + 1); n.urgent = true; s.cards.push(n);
      return 'Urgent request – new task #' + n.id + ' lands in Not Started.';
    }
    if (draw === 'rework') {
      // Only started tasks can be sent back; done is done.
      var started = chosen && chosen.col === 'ip' ? [chosen] : s.cards.filter(function (c) { return c.col === 'ip'; });
      if (started.length) {
        var d = pick(r, started); d.col = 'ns'; d.rework = true;
        s.lost = (s.lost || 0) + d.hours; d.hours = 0; // the thrown-away hours are waste even if the task is finished later
        return 'Someone wants changes to #' + d.id + ' – back to Not Started. The hours already put in are lost.';
      }
      return 'Changes are requested before anything is started – the hour is lost.';
    }
    return null;
  }

  // One turn. Returns a log entry describing what happened.
  function step(s, draw, player, r, opt) {
    s.turn++;
    var cand = candidates(s, opt);
    var blocked = s.cards.filter(function (c) { return c.col === 'bl'; });
    var e = { turn: s.turn, player: player, draw: draw, chosen: null, action: '' };

    if (!cand.length) {
      var ev0 = teamEvent(s, draw, null, r);
      if (ev0) { e.action = ev0; s.log.push(e); return e; }
      if (draw === 'breakthrough' && blocked.length) {
        var b0 = pick(r, blocked); b0.col = 'ip';
        e.action = 'No task to choose. Lifts the block on #' + b0.id + '.';
      } else {
        s.idle++;
        e.action = 'No task can be chosen – the player waits.';
      }
      s.log.push(e); return e;
    }

    var c = pickTask(s, r, cand, player, opt);
    e.chosen = c.id;
    var ev = teamEvent(s, draw, c, r);
    if (ev) { e.action = ev; s.log.push(e); return e; }
    if (c.col === 'bl') { // chasing an external block
      if (draw === 'smooth' || draw === 'breakthrough') {
        c.col = 'ip'; e.action = 'Chases the outside party – #' + c.id + ' is unblocked.';
      } else e.action = 'Chases #' + c.id + ', but the answer has not come yet.';
      s.log.push(e); return e;
    }
    if (draw !== 'breakthrough') c.hours++;
    if (draw === 'smooth') {
      c.col = c.col === 'ns' ? 'ip' : 'done';
      e.action = c.col === 'ip' ? 'Starts #' + c.id + '.' : 'Finishes #' + c.id + '.';
    } else if (draw === 'breakthrough') {
      if (blocked.length && r() < opt.pLift) {
        var b = pick(r, blocked); b.col = 'ip';
        e.action = 'Leaves #' + c.id + ' and lifts the block on #' + b.id + '.';
      } else {
        c.hours++; c.col = 'done';
        e.action = 'Finishes #' + c.id + ' in one go.';
      }
    } else if (draw === 'dependency') {
      c.col = 'ip';
      var targets = s.cards.filter(function (o) {
        // Not a blocked task, and not one that another task already waits for: each dependency is unique.
        return o.id !== c.id && o.col !== 'done' && o.col !== 'bl' && !isHelper(s, o) && !reaches(s, o.id, c.id);
      });
      if (targets.length) {
        c.dep = pick(r, targets).id;
        e.action = '#' + c.id + ' turns out to need #' + c.dep + ' first.';
      } else {
        e.action = '#' + c.id + ' gets an hour of work, nothing else to wait for.';
      }
    } else if (draw === 'longer') {
      if (c.owner === null) c.owner = player;
      e.action = '#' + c.id + ' takes longer than planned – the hour goes in, the task does not move.';
    } else if (draw === 'external') {
      c.col = 'bl';
      e.action = '#' + c.id + ' waits for someone outside the team.';
    }
    if (c.owner === null && c.col !== 'ns') c.owner = player;
    if (c.col === 'done' && c.owner !== player) {
      s.collab++;
      e.action += ' (started by player ' + c.owner + ')';
    }
    s.log.push(e); return e;
  }

  // Plays a whole game. onTurn(state, entry) is called after every turn (for animation).
  function play(opt, onTurn) {
    opt = Object.assign({ tasks: 16, players: 4, wip: null, blockedCountsWip: false,
      pLift: 0.5, chaseBlocked: false, pNew: 0.5, collab: 'high', pull: false, planning: false, planKeep: 1 / 3,
      seed: 1, choiceSeed: null, deck: DECK }, opt);
    var deck = shuffledDeck(opt.seed, opt.deck);
    var r = rng(opt.choiceSeed === null ? opt.seed * 7919 + 13 : opt.choiceSeed);
    var s = newState(opt.tasks);
    // With planning the first round (one turn per player) goes to planning. The game is as long
    // as without it, so cards are drawn from turn players+1 and the last `players` cards are never drawn.
    var plan = opt.planning ? plannedDeck(deck, opt.seed, opt.planKeep) : { deck: deck, planned: {} };
    var drawn = [];
    deck.forEach(function (d, i) {
      var player = (i % opt.players) + 1, e;
      if (opt.planning && i < opt.players) { e = planTurn(s, player); drawn.push(null); }
      else {
        var k = opt.planning ? i - opt.players : i;
        e = step(s, plan.deck[k], player, r, opt);
        if (plan.planned[k]) { e.planned = true; e.action += ' (planning avoided a ' + (plan.planned[k] === 'longer' ? 'task taking longer' : 'dependency') + ')'; }
        drawn.push(plan.deck[k]);
      }
      if (onTurn) onTurn(s, e);
    });
    return { state: s, deck: deck, drawn: drawn, result: summary(s) };
  }

  function summary(s) {
    var n = function (col) { return s.cards.filter(function (c) { return c.col === col; }).length; };
    return { done: n('done'), inProgress: n('ip'), blocked: n('bl'), notStarted: n('ns'),
      waitingDep: s.cards.filter(function (c) { return c.col !== 'done' && depActive(s, c); }).length,
      idle: s.idle, collab: s.collab, tasks: s.cards.length, waste: waste(s) };
  }

  // Lean waste: hours put into tasks that did not reach Done.
  function waste(s) {
    return (s.lost || 0) + s.cards.reduce(function (a, c) { return a + (c.col === 'done' ? 0 : c.hours); }, 0);
  }

  function stats(opt, runs) {
    var keys = ['done', 'inProgress', 'blocked', 'notStarted', 'idle', 'collab', 'tasks', 'waste'];
    var sum = {}, hist = [];
    keys.forEach(function (k) { sum[k] = 0; });
    for (var i = 0; i < runs; i++) {
      var res = play(Object.assign({}, opt, { seed: 100000 + i, choiceSeed: 900000 + i })).result;
      keys.forEach(function (k) { sum[k] += res[k]; });
      hist[res.done] = (hist[res.done] || 0) + 1;
    }
    var avg = {};
    keys.forEach(function (k) { avg[k] = sum[k] / runs; });
    avg.hist = hist;
    return avg;
  }

  var CK = { DECK: DECK, CARD_TEXT: CARD_TEXT, play: play, stats: stats, summary: summary,
    shuffledDeck: shuffledDeck, candidates: candidates, wipCount: wipCount,
    isHelper: isHelper, depActive: depActive };
  if (typeof module !== 'undefined' && module.exports) module.exports = CK;
  else root.CK = CK;
})(this);
