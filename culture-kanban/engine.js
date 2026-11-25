// Culture Kanban – simulation engine. Pure functions, no DOM.
// Works in the browser (window.CK) and in node (module.exports).
(function (root) {
  'use strict';

  var DECK = { smooth: 18, breakthrough: 2, dependency: 10, external: 2 };
  var CARD_TEXT = {
    smooth: 'Smooth hour – move the chosen task one step.',
    breakthrough: 'Breakthrough – finish the chosen task, or lift an external block.',
    dependency: 'Dependency – the chosen task turns out to need another task first.',
    external: 'External block – the chosen task waits for someone outside the team.'
  };

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
    for (var i = 0; i < nTasks; i++) cards.push({ id: i + 1, col: 'ns', dep: null });
    return { cards: cards, turn: 0, idle: 0, log: [] };
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

  // One turn. Returns a log entry describing what happened.
  function step(s, draw, player, r, opt) {
    s.turn++;
    var cand = candidates(s, opt);
    var blocked = s.cards.filter(function (c) { return c.col === 'bl'; });
    var e = { turn: s.turn, player: player, draw: draw, chosen: null, action: '' };

    if (!cand.length) {
      if (draw === 'breakthrough' && blocked.length) {
        var b0 = pick(r, blocked); b0.col = 'ip';
        e.action = 'No task to choose. Lifts the block on #' + b0.id + '.';
      } else {
        s.idle++;
        e.action = 'No task can be chosen – the player waits.';
      }
      s.log.push(e); return e;
    }

    var c = pick(r, cand);
    e.chosen = c.id;
    if (c.col === 'bl') { // chasing an external block
      if (draw === 'smooth' || draw === 'breakthrough') {
        c.col = 'ip'; e.action = 'Chases the outside party – #' + c.id + ' is unblocked.';
      } else e.action = 'Chases #' + c.id + ', but the answer has not come yet.';
      s.log.push(e); return e;
    }
    if (draw === 'smooth') {
      c.col = c.col === 'ns' ? 'ip' : 'done';
      e.action = c.col === 'ip' ? 'Starts #' + c.id + '.' : 'Finishes #' + c.id + '.';
    } else if (draw === 'breakthrough') {
      if (blocked.length && r() < opt.pLift) {
        var b = pick(r, blocked); b.col = 'ip';
        e.action = 'Leaves #' + c.id + ' and lifts the block on #' + b.id + '.';
      } else {
        c.col = 'done';
        e.action = 'Finishes #' + c.id + ' in one go.';
      }
    } else if (draw === 'dependency') {
      c.col = 'ip';
      var targets = s.cards.filter(function (o) {
        return o.id !== c.id && o.col !== 'done' && !reaches(s, o.id, c.id);
      });
      if (targets.length) {
        c.dep = pick(r, targets).id;
        e.action = '#' + c.id + ' turns out to need #' + c.dep + ' first.';
      } else {
        e.action = '#' + c.id + ' gets an hour of work, nothing else to wait for.';
      }
    } else if (draw === 'external') {
      c.col = 'bl';
      e.action = '#' + c.id + ' waits for someone outside the team.';
    }
    s.log.push(e); return e;
  }

  // Plays a whole game. onTurn(state, entry) is called after every turn (for animation).
  function play(opt, onTurn) {
    opt = Object.assign({ tasks: 16, players: 4, wip: null, blockedCountsWip: false,
      pLift: 0.5, chaseBlocked: false, seed: 1, choiceSeed: null, deck: DECK }, opt);
    var deck = shuffledDeck(opt.seed, opt.deck);
    var r = rng(opt.choiceSeed === null ? opt.seed * 7919 + 13 : opt.choiceSeed);
    var s = newState(opt.tasks);
    deck.forEach(function (d, i) {
      var e = step(s, d, (i % opt.players) + 1, r, opt);
      if (onTurn) onTurn(s, e);
    });
    return { state: s, deck: deck, result: summary(s) };
  }

  function summary(s) {
    var n = function (col) { return s.cards.filter(function (c) { return c.col === col; }).length; };
    return { done: n('done'), inProgress: n('ip'), blocked: n('bl'), notStarted: n('ns'),
      waitingDep: s.cards.filter(function (c) { return c.col !== 'done' && depActive(s, c); }).length,
      idle: s.idle };
  }

  function stats(opt, runs) {
    var keys = ['done', 'inProgress', 'blocked', 'notStarted', 'idle'];
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
