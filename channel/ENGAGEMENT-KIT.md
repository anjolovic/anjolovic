# Then What? — Engagement kit

The per-video system that turns a view into a subscriber, a like, a share and a comment. Every
episode ships with all seven parts. Nothing here is optional and nothing here is clever: the same
asks, in the same slots, every time, so the audience learns the shape.

Why these slots. YouTube ranks on watch time and on how many people act on a video, and it weighs
early actions heavily. A subscribe ask before the viewer has received anything is ignored; one
right after the first payoff converts. A comment prompt works when it asks a question the viewer
already has an answer to. A share ask works when it names the person to send it to.

---

## 1. In the video: three fixed lines (brand record §4)

| Slot | When | Line | Why here |
|---|---|---|---|
| **Subscribe** | Right after the first payoff, about 1:15, one sentence, then straight back into the story | "If you're new here, subscribe. This is what we do: what happens next, minute by minute." | The viewer just got something. Ask once, early, briefly. Never at the top, never twice |
| **Comment** | The personalisation beat: the moment the scenario maps onto the viewer's own life (the temperature fork, the window-or-aisle choice) | "Tell me in the comments: [the episode's one question]." | Asks for a fact the viewer already has, not an opinion they have to form |
| **Like and share** | Outro, before the next-video pointer | "If you learned something today, hit like and send this to [the person who needs it]." | Names a recipient. "Share" alone is abstract; "the nervous flyer in your life" is a person |

Then the pointer to the next episode, then the sign-off: "That's what. See you in the next one."

The delivered 2:00 cuts have no room for spoken asks; for those three videos the description,
pinned comment, cards and end screen carry the whole load.

## 2. Description template

The first two lines show above the fold and in search; they are the hook and the stat, nothing
else. The subscribe link uses `?sub_confirmation=1`, which opens a confirm-subscribe dialog.

```
[Second-person hook, one sentence, present tense.] [The one number that makes it real.] Here is [payoff 1], [payoff 2], and [the one rule].

Subscribe for what happens next, minute by minute: https://www.youtube.com/@thenwhattvshow?sub_confirmation=1

⏱ Chapters
0:00 [chapter]
[...at least three, first at 0:00, each 10 s or longer]

The rule to remember: [one line].

[The episode's comment question]? Tell me in the comments.

Next: [next episode title]. Playlist: [pillar playlist URL].

This video is for general information and is not a substitute for professional [safety] training. Figures are rounded; [what varies] varies by source and by conditions.

Sources and further reading:
[Source] — [URL]
[...]

Footage in this video is AI-generated to illustrate the scenario. No real incident is depicted.

#[topic] #survival #thenwhat
```

## 3. Pinned comment template

Post it the moment the video goes live, from the channel, and pin it. Heart the first ten
sensible replies inside the first hour; hearted replies notify their authors and pull them back.

```
The whole video in five lines:
1. [recap line]
2. [recap line]
3. [recap line]
4. [recap line]
5. [recap line]

[The boring truth, one sentence.] [The comment question]?
```

## 4. Cards

Two per long-form episode, both aligned to the beats where a viewer is most likely to stay:

| Card | When | Points to |
|---|---|---|
| 1 | The first mini-cliff (~3:15 long-form, ~0:50 in the 2:00 cuts) | The most related episode in the same pillar |
| 2 | The twist / second mini-cliff (~6:20 long-form, ~1:40 in the 2:00 cuts) | The pillar playlist |

## 5. End screen (last 20 seconds)

Ground: `brand/out/end-screen-1920x1080.png` or the episode's own calm final shot. Elements,
placed in Studio in this layout: next episode (video element, left), subscribe (right,
circular), pillar playlist (below). The narration's last words are the sign-off, so the
subscribe element is on screen while "That's what" lands.

Video element rule: point at a specific next episode, never "best for viewer", so the chain
through the pillar is deliberate. Update the previous episode's end screen the day a new one
goes live.

## 6. Off-video cadence

| When | What |
|---|---|
| Publish day, T+0 | Community post: thumbnail A plus two sentences and the comment question. Pinned comment live. Previous episode's end screen re-pointed at this one |
| T+1 day | Shorts cut 1 (the hook, 9:16 reframe, Shorts stamp on top). Description: the long-form link and "Full episode on the channel". Shorts comment pinned with the link |
| T+2 days | Shorts cut 2 (the twist). Community poll built on the comment question, two to four options |
| T+3 days | Reply pass: answer every question in the comments that has a factual answer; heart good replies |
| T+7 days | Next episode. Repeat |

## 7. Retrofit for the three delivered cuts

Applied in this pass to `../production/YOUTUBE-PACKAGE.md`, `../production/freezer/YOUTUBE-PACKAGE.md`
and `../production/elevator/YOUTUBE-PACKAGE.md`: subscribe link and comment question added to each
description, pinned comments extended with the question, end screens pointed at a named next
episode. The 2:00 narration is unchanged; it is already rendered.

Applied to the two long-form scripts (`../brightside-video-script.md`, `../production/pilot/SCRIPT.md`):
the subscribe line after the first payoff, the comment prompt at the personalisation beat, and the
like-and-share line in the outro.

## 8. What to measure (Analytics, weekly)

- Subscribers gained from each video, per 1,000 views. The subscribe ask at 1:15 should show as a small step in the "subscribers" timeline.
- Audience retention at 1:15 and at each mini-cliff. A dip at the ask means it is too long; it should be one sentence.
- Comments per 1,000 views. The comment question should lift this above the channel average; if it does not, the question is an opinion, not a fact.
- Shares per 1,000 views. If the named recipient does not move it, name a more specific one.
