# What I Wish I Knew When I Started Doing Experimental Nucear Physics

## Introduction

The idea for this document came during a conversation with Sean Dobbs in which I was lamenting that I finally, in year 7 of my PhD, started implementing good software practices into my analysis workflow. While it's better that I learned and used these things later rather than never, I was frustrated that extremely useful and important practices such as, "writing functions", and, "using github" weren't taught to me when I joined the ODU Nuclear Phyiscs research group. Now, It's not Dr. Amaryan or Dr Kuhn's fault - it's not their job to teach us these things; their job is to teach us physics, not software engineering - but it is frustrating nonetheless.

During the aforementioned lamenting, Sean told me:

> maybe if you have time, you should write a short presentation or wiki page of "software things I wish I had known when I started out as a grad student", to help others out

This document is my attempt at that. While thinking about knowledge I wanted to pass on to the newest generation of ~~underpaid code monkeys~~ graduate students, I realized that the scope of that "wisdom" extends beyond good coding practices. 

To whomever reads this, I hope you find it useful. It's not comprehensive, and it's not gospel. It's just a collection of things I wish I knew when I started doing experimental nuclear physics.

## The Basics
Welcome to the world of experimental nuclear physics! When you tell your family/friends/enemies/strangers what you do, the first thing that they will ask you inevitably will be "oh so like, making bombs?" 

No, not like making bombs. 

What we do, day to day, is *write code*. Signifigantly less impressive, huh? What you will do, day to day, is write code to perform a host of tasks. That code can be data analysis, data acquisition, data simulation, or any number of other things, but you will be writing code. This is your life now. 

Many, though not all, of course, are not really prepared for this reality. Many, though not all, have fairly limited programming experience, especially *practical* experience - what we do obviously goes beyond:
```cpp
cout << "Hello World!" << endl;
```
So my absolute first piece of advice is this: **learn to code**.

### Learn to Code
Learning how to code, not just learning how to use `ROOT` or `GEANT4` or whatever it is your project will require, is, in my opinion, vitally important. Understanding the basics of programming, and how to write good code, will make your life much, much easier in the long run. 

