---
publish: true
title: Role-playing Test
created: 2026-07-24T12:30:26.406+02:00
modified: 2026-07-24T12:33:00.000+02:00
tags:
  - "#process"
  - "#designprocess"
  - "#iterativedesign"
  - "#game-design"
  - "#ttrpg"
  - "#play_test"
  - "#ai"
  - "#AI-agents"
  - "#infernal_ventures"
---
![[6. Verktyg/Attached/Recon Pioneers-1.png]]

Designing role-playing games is slightly harder than many other games. Or so I claim, at least. Because during the playtest itself, there are so many factors that influence the outcome and the experience. I am currently testing a game called [[premiss.en|Infernal Ventures]]. And I have made great progress.

The problem with playtesting role-playing games is actually quite human: it requires people. Not only the fact that to try a single rule change, I need to gather a bunch of friends around a table, set aside an evening, and then hope that the specific situation I want to test actually arises during the game. And if it doesn't, then it was an evening spent on something else. Fun something else, often – but not what I wanted to investigate. Furthermore, very few of my role-playing friends care about the system. They are there for the story.
Then we have the general problem of determining whether the role-playing experience was good or bad. It can be due to my performance as a game master, it can be due to the rules not quite delivering what they should, it can be due to my players not understanding and continuing to play as if it were something else and ignoring my silly rules. Extremely difficult to determine in any case.

For this reason, I have built a small simulation of my new (card-driven) [[Speldesign|role-playing system]]. I sit as the game master in the browser, and instead of my friends, various AIs play the players. I describe a conflict, a scene, an obstacle – and then the AI characters attempt to get through it. I see which cards they choose, how they build their hand, what is drawn, and I can judge exactly as I would have at the table: no, that skill doesn't work here, try something else. I also understand how the system behaves generally – for example, if there's a strategy that breaks the system or if it's impossible to get out of a stalemate. I could have built a probability machine that showed how the system behaves with a Python script, but it's very difficult to understand how rules affect the narrative. That's where my role-playing AI agents come in.

The point is not that the AI plays good role-playing games – it's so-so at that. The point is that I can run the same scene ten times in an afternoon and see if the mechanics behave as I hoped. Does the draw build towards a climax? Does a certain card type get drowned out? Does the cost of success feel right? And as I mentioned earlier - are rule outcomes transformed into an interesting story – i.e., does the AI agent phrase the outcome in a way that makes the game work? Things that would otherwise take months of playtesting to even suspect, I can see directly.

Don't get me wrong – it doesn't replace the real table. An AI feels no tension, takes no reckless risks for fun, and isn't disappointed when things turn. But as a workshop where I can [[Designprocess.en|tweak the rules between each attempt]], it is invaluable. Much like the difference between serving an untested recipe at a dinner party and being able to taste it as you cook.
