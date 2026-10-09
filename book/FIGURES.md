# Figures in the library: markup for writers

Write figures as plain HTML inside a section file. The reader numbers them ("Figure 3.4"), styles them for paper, sepia and night themes, and fits them to phone width.

Every figure follows the same rules:
- It opens with a `<figcaption>` holding its title: a short phrase that says what the figure shows.
- It closes with `<p class="fig-src">`, holding the `[cite:key]` notes for everything it shows.
- It shows only what those sources support. Keep labels short (under about 60 characters) and details to one line.

Place a figure right after the paragraph that introduces it. The prose must still make sense without it.

## Process flow: a mechanism or chain of decisions (at most 7 steps)
```html
<figure class="fig-flow">
<figcaption>How a Mandate was conferred</figcaption>
<ol>
<li><b>Allied Supreme Council, San Remo</b> Assigns the Mandate for Palestine to Britain, April 1920</li>
<li><b>Council of the League of Nations</b> Approves the Mandate text, July 1922</li>
<li><b>Britain</b> Administers Palestine under the Mandate's terms</li>
</ol>
<p class="fig-src">Sources: [cite:key1] [cite:key2]</p>
</figure>
```

## Money chain: who paid, through what, to whose gain and at whose cost
There are always five steps, in this order. The reader adds the step labels: Where it came from, How it moved, What multiplied it, Who gained, Who bore the cost.
```html
<figure class="fig-money">
<figcaption>The Keren Hayesod funding chain</figcaption>
<ol>
<li><b>Donors in the diaspora</b> Annual campaigns from 1920</li>
<li><b>Keren Hayesod</b> Permanent fund of the Zionist Organization</li>
<li><b>…</b> …</li>
<li><b>…</b> …</li>
<li><b>…</b> …</li>
</ol>
<p class="fig-src">Sources: [cite:key]</p>
</figure>
```

## Timeline: dated events in order
```html
<figure class="fig-time">
<figcaption>Three promises, 1915–1917</figcaption>
<ol>
<li><time>1915–16</time><b>Hussein–McMahon correspondence</b> British pledge of Arab independence, with exclusions</li>
<li><time>May 1916</time><b>Sykes–Picot</b> Secret Anglo-French division of the region</li>
<li><time>2 Nov 1917</time><b>Balfour Declaration</b> Support for a Jewish national home in Palestine</li>
</ol>
<p class="fig-src">Sources: [cite:key]</p>
</figure>
```

## Comparison: two documents, two accounts, a claim and the record (at most 4 columns)
```html
<figure class="fig-compare">
<figcaption>The Balfour Declaration and the Mandate text</figcaption>
<table>
<thead><tr><th></th><th>Balfour, 1917</th><th>Mandate, 1922</th></tr></thead>
<tbody>
<tr><th>Legal status</th><td>A letter</td><td>An instrument of the League of Nations</td></tr>
</tbody>
</table>
<p class="fig-src">Sources: [cite:key]</p>
</figure>
```
Mark a cell `class="yes"` or `class="no"` only where the record is a plain yes or no.

## Power structure: who sat above whom
```html
<figure class="fig-tree">
<figcaption>Who governed Mandate Palestine, 1922</figcaption>
<ul>
<li><b>League of Nations</b> Supervises through the Permanent Mandates Commission
  <ul>
  <li><b>British Government, Colonial Office</b> Responsible for the Mandate
    <ul>
    <li><b>High Commissioner</b> Governs in Jerusalem</li>
    <li><b>Zionist Organization</b> The recognized "Jewish agency" under Article 4</li>
    </ul>
  </li>
  </ul>
</li>
</ul>
<p class="fig-src">Sources: [cite:key]</p>
</figure>
```
Use at most 4 levels and 8 boxes.

## Key figures: the numbers a section turns on (2 to 6)
```html
<figure class="fig-stats">
<figcaption>Palestine in 1922</figcaption>
<dl>
<div><dt>757,182</dt><dd>Total population, 1922 census</dd></div>
<div><dt>11%</dt><dd>Jewish share of the population</dd></div>
</dl>
<p class="fig-src">Sources: [cite:key]</p>
</figure>
```
(The values above only show the format. Use the source's own numbers.)

## Network
Drawn automatically from the section's people, institutions and documented ties. No markup is needed.
