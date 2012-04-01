
VIRON
=====

A dead-stupid templating utility script that simple-mindedly replaces
$ENVIRONMENT_VARIABLE-ishy tokens with the contents of the environment
variable of the same name. By "-ishy" I mean "the subset of environment
variables whose names you can express with only capital letters, plus numerals
and underscores after the first character".

E.g.:

    $YOU_CAN_USE_ME
    $I2MOK
    $_NO_DICE_IN_MY_CASE
    $IWontFlyEither

Viron handles curly-braces and backslash escapes for dollar signs work as you have
no doubt come to expect, e.g.:

    $I_BECOME_MY_CONTENT
    \$WHEREAS_I_REMAIN_UNAFFECTED
    ${I_LOVE_YOU}BUT_I_HAVE_BOUNDARIES

Viron works hard to be this straightforardly stupid. For example, Viron is implemented
on top of the python standard-lib [string.Template class](http://docs.python.org/release/2.5.2/lib/node40.html), which idiotically takes
the liberty of turning any occurances of doubled-up dollar signs (or '$$') into
a single dollar sign (to wit, '$') that it should happen across while templating... Viron 
specifically lacks this nonsensical 'feature'.

Conversely, the stdlib templater's vexing ignorance of the backslash prefix to mean
"this token is stripped of its power by my fiat, fuck the standard semiotic intent"
by nearly all contemporary civilized programming languages. The idea is that Viron
doesn't want to over-explain itself, so anything consistent with the "environment-variable
template syntax" concept is in, like backslashes; notions requiring
additional bullet points have been cut, with the most ruthless vetos going to
questionable shit like "silently fucking with the number of dollar signs in your
file in a way you might not immediately notice" and suchlike.

And so yeah, this was a very deliberate "software architecture" decision, so you can
relax right now and go about your business without worrying if I have heard of one
of the other eleventy billion scripts, tools, frameworks, plug-ins, or thingees that
accomplish this exact task except better or moreso or someshit. Viron isn't some
kind of freakish zombified imperative markup like [HAML](http://haml-lang.com/), nor is it something wittily
elegant that up and becomes a gosh-darned de-facto standard, such as for example
[Mustache](http://mustache.github.com/). It's just dumb ol' environment variables in text files -- truth be told,
I didn't even want to write it, but I keept needing it and none of the other solutions
were stupid enough.

And so! That said, I do love you and your contributions to open source, so please do
feel free to fork it up and subsequently request pulls, I would be thrilled at any
work you may have to contribute! I'm not even gonna say no if you take it the other
way entirely and send me a patch titled "Viron is now turing-complete and implements
semantically legible Oauth2 and free foot-rubs" I will probably totally accept it.
Realistically, you're going to hack on stuff with more cachét, like e.g.

* demoing a realtime notification framework and protocol that uses at least three NoSQL stores simultaneously
* sharing clever Haskell type-inference schemes with other people who also write clever Haskell type-inference schemes
* not subclassing NSActionCell, staying in denial by writing convenience methods all day and only touching your app's mongoloid UI in the simulator
* punching Rasmus Lerdorf in the kidneys (q.v. backslash note ¶4 [supra])
* "writing" incoherent and Byzantine Oauth2 examples that do not clarify the issue or condescend to explain what all the bits are, why in fuck those bits are there, or why they are fucking different from some (but not all) of the bits on this other different Oauth2 example over here
* pair-programming behavior-driven domain-specific social-graph microframeworks pivoting on a responsive user-experience, in the cloud

... So but if Viron can actually work for you, I am quite literally and unsarcastically thrilled on your behalf -- do let me know, and salud.