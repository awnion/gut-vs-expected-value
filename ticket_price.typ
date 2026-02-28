#set text(lang: "en", size: 11pt)
#set page(
  margin: (left: 10mm, right: 10mm, top: 14mm, bottom: 14mm),
  paper: "a4",
)
#set par(justify: true, leading: 0.65em)

// Helper: text content with comfortable reading width
#let narrow(body) = pad(left: 20mm, right: 20mm, body)

// --- PAGE 1: Hook + Problem + Graph ---

#narrow[
  #block(
    fill: luma(242),
    inset: 20pt,
    radius: 6pt,
    width: 100%,
  )[
    #text(size: 14pt)[
      Imagine two buttons in front of you.
    ]

    #v(0.7em)

    #grid(
      columns: (1fr, 1fr),
      gutter: 12pt,
      align(center)[
        #text(fill: rgb("#c62828"), weight: "bold", size: 20pt)[🔴 Red]
        #v(0.3em)
        #text(size: 13pt)[50% chance to win *\$100X*]
      ],
      align(center)[
        #text(fill: rgb("#2e7d32"), weight: "bold", size: 20pt)[🟢 Green]
        #v(0.3em)
        #text(size: 13pt)[100% chance to receive *\$X*]
      ],
    )

    #v(0.7em)

    #text(size: 14pt)[
      You can play yourself or sell the ticket. The question is: *for how much?*
    ]
  ]

  #v(0.6em)

  The expected value of the red button is $bb(E) = 50 X$, which is 50 times the
  green one. Sounds like an easy choice. But plug in real numbers: $X =$
  \$1,000,000. Would you really walk away from a guaranteed million for a coin
  flip on a hundred million?

  Most people wouldn't. And they're not being irrational.

  #v(0.3em)

  == Why the price depends on who's buying

  Every next dollar brings a little less joy than the previous one. A million to
  a student is a life-changing event. A million to a billionaire is a rounding
  error. This is called *diminishing marginal utility*, and it's the reason
  people are cautious with large bets.

  With logarithmic utility (a classical model that fits real behavior reasonably
  well), the "fair price" of the red button for someone with wealth
  $italic("Wealth")$ is:

  $
    "Certainty Equivalent" = sqrt(italic("Wealth") dot (italic("Wealth") + 100X)) - italic("Wealth")
  $

  The ticket price is $max("Certainty Equivalent", X)$, because the green button
  sets the floor.
]

#v(0.3em)

#figure(
  image("img/ticket_price_plot.svg", width: 100%),
  caption: [Left: absolute ticket price by buyer wealth (log scale). Right:
    ticket price as percentage of $bb(E)[X]$. Red line: approximate market
    price.],
)

// --- PAGE 2: Analysis ---

#narrow[
  == Who pays what

  #figure(
    table(
      columns: (auto, auto, auto),
      align: (left, right, right),
      table.header([*Buyer's Wealth*], [*Ticket Price*], [*Share of* $bb(E)$]),
      [$100 X$], [$approx 41 X$], [82%],
      [$10 X$], [$approx 23 X$], [46%],
      [$X$], [$approx 9 X$], [18%],
      [$0.1 X$], [$approx 2.2 X$], [4.4%],
    ),
  )

  The pattern is simple: the smaller the bet relative to your net worth, the
  closer you get to the "rational" $50 X$. The larger it is, the more you want
  to press green.

  #v(0.3em)

  == What happens on a real market

  In a market with many participants, the price isn't set by the average buyer.
  It's set by *the most risk-tolerant one*, the person for whom the stakes feel
  small. A rough approximation:

  $ "Price" approx (50 X) / (1 + 1.5 dot X / italic("Wealth")_"median") $

  When $X$ is small, the price approaches $50 X$. When $X$ is large, it
  collapses toward $X$.

  == What experiments tell us

  Kahneman and Tversky showed that real people deviate from the logarithmic
  model in a predictable way. The guaranteed $X$ you have to give up doesn't
  feel like a missed opportunity. It feels like a *loss*. And losses hurt
  roughly twice as much as equivalent gains, which pushes the price down even
  further.

  For calibration: a typical person behaves with a risk aversion coefficient
  $gamma approx 1 "–" 2$. Financial professionals sit around
  $gamma approx 0.5 "–" 1$. Some people hit $gamma approx 3 "–" 5$, and for them
  even a modest red button looks terrifying.

]

#figure(
  image("img/violin_plot.svg", width: 100%),
  caption: [Distribution of "fair" ticket prices (as % of $bb(E)$) across a
    simulated population (log-normal wealth, median \$60K). The wider the shape,
    the more people cluster at that price. Red diamond: approximate market
    clearing price. The bigger the game, the steeper the discount.],
)
