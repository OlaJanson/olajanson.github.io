---
publish: true
title: Rollspelstest
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

Att designa rollspel är aningen svårare än många andra spel. Eller det hävdar jag i alla fall. För under själva speltestet är det så många faktorer som påverkar utfallet och upplevelsen.  Jag håller just för tillfället på att testa ett spel som heter [[premiss|Infernal Ventures]]. Och jag har gjort stora framsteg

Problemet med att speltesta rollspel är egentligen ganska mänskligt: det kräver människor.  Inte bara det faktum att jag för att pröva en enda regeländring behöver jag samla ett gäng vänner runt ett bord, sätta av en kväll, och sedan hoppas att just den situation jag vill testa faktiskt dyker upp under spelets gång. Och gör den inte det så var det en kväll som gick till annat. Roligt annat, oftast – men inte det jag ville undersöka. Dessutom är det så att jag väldigt få av mina rollspelande vänner bryr sig om systemet. De är där för berättelsen.
Sedan har vi det generella problemet med att avgöra ifall upplevelsen av rollspelet var bra eller dålig. Det kan bero på min prestation som spelledare, det kan bero på att reglerna inte riktigt leverera det de skall, det kan bero på att mina spelare inte fattar och fortsätter spela som om det var något annat och struntar i mina fåniga regler. Oerhört svårt att avgöra i alla fall.

Med anledning av detta så har jag byggt en lite simulering av mitt ny (kortdrivna) [[Speldesign|rollspelssystem]].  Jag sätter mig som spelledare i webbläsaren, och i stället för mina vänner är det olika AI som spelar spelarna. Jag beskriver en konflikt, en scen, ett hinder – och så spelar AI  karaktärerna försök att ta sig igenom det. Jag ser vilka kort de väljer, hur de bygger sin hand, vad som dras, och jag kan döma precis som jag skulle gjort vid bordet: nej, den där färdigheten håller inte här, prova något annat. Jag förstår också hur systemet beter sig rent generellt – till exempel att det finns något strategi som knäcker systemet eller om det aldrig går att komma ur ett dödläge. En sannolikhetsmaskin som visade hur systemet beter sig hade jag klarat av att bygga med ett python-script men det är väldigt svårt att förstå hur regler påverkar narrativet. Det är där mina rollspelande ai-agenter kommer in.

Poängen är inte att AI:n spelar bra rollspel – det gör den sådär. Poängen är att jag kan köra samma scen tio gånger på en eftermiddag och se om mekaniken beter sig som jag hoppades. Bygger dragningen mot ett klimax? Drunknar en viss korttyp? Känns priset för att lyckas rätt? Och som jag tidigare nämnde - omvandlas regelutfall till en intressant berättelse – dvs klär Ai-agenten utfallet i ord på ett sätt så att spelet funkar? Sånt som annars tar månader av speltest att ana får jag syn på direkt.

Missförstå mig rätt – det ersätter inte det riktiga bordet. En AI känner ingen spänning, tar inga dumdristiga risker för att det är kul, och blir inte besviken när det vänder. Men som en verkstad där jag kan [[Designprocess|skruva på reglerna mellan varje försök]] är den ovärderlig. Ungefär som skillnaden mellan att servera ett oprövat recept på en middagsbjudning och att få smaka av under tiden man lagar.
