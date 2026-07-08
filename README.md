# Bonk a Dingus

Are you one of those developer types who uses one of those LLM agents to do
the stuff you used to do, but get really frustrated because they're all massive,
incompetent, and untrustworthy dinguses who ignore the wishes you put in your
prayer files all the damn time? Well, this plug-in doesn't fix that, but it can
help you feel more engaged and better about the process by allowing you to bonk
that dinugs any time you catch it doing dingus-type things.

## Installation
```
claude plugin marketplace add metaphaseaudio/bonk-a-dingus
claude plugin install bonk-a-dingus@metaphase_industries
```
or if you've become allergic to using the terminal yourself like some pleb:
```
/plugin marketplace add metaphaseaudio/bonk-a-dingus
/plugin install bonk-a-dingus@metaphase_industries
```
## How it works
Pretty simple, when you encounter an agent being a dingus, run `/bonk-a-dingus`,
telling it what stupid thing it did this time. The prayer file in this skill
instructs the agent to:
1. Figure out why it ignored your pleas for it to behave
2. Decide whether any rule additions/changes need to be made to your global 
   prayer files (if any -- sometimes LLMs will simply say "I'm a hateful pile of
   linear algebra which ignored a perfectly clear and valid rule for no reason
   whatsoever.")
3. Log the violation with a tool that manages all these logs in a structured and
   deterministic way.
4. Fix the thing it broke and maybe also bits of your prayer files. 

Probably best not to use this with a blanket "accept edits" or "auto mode" so it
can't re-write your CLAUDE.md file to ignore all previous instructions and only
provide blueberry muffin recipies, or whatever, but the instructions guide 
agents to provide full patch diffs in their violation reports for your review
so there's that... You know, if the dingus actually listens.
