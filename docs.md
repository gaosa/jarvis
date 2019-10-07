## Encoding

### Encoding Data Types
|Data Type|Shorthand Code|Description|
|-|-|-|
|quantitative|`Q`|A continuous real-valued quantity|
|ordinal|`O`|A discrete ordered quantity|
|nominal|`N`|A discrete unordered category|
|temporal|`T`|A time or date value|

### Encoding Channels
|Channel|Altair Class|Description|
|-|-|-|
|color|Color|The color of the mark|
|size|Size|The size of the mark|
|order|Order|Sets the order of the marks|
|column|Column|The column of a faceted plot|
|row|Row|The row of a faceted plot|

### Encoding Channel Options
The `X` and `Y` encodings accept the following options:

|Property|Type|Description|
|-|-|-|
|stack|anyOf(`StackOffset`, `null`, `boolean`)|Type of stacking offset if the field should be stacked. `stack` is only applicable for `x` and `y` channels with continuous domains. For example, `stack` of `y` can be used to customize stacking for a vertical bar chart. `stack` can be one of the following values: `"zero"` or `true`, `"normalize"`, `"center"`, `null` or `false`.|

## Marks
|Mark Name|Method|Description|
|-|-|-|
|area|`mark_area()`|A filled area plot|
|bar|`mark_bar()`|A bar plot|
|circle|`mark_circle()`|A scatter plot with filled circles|
|line|`mark_line()`|A line plot|
|point|`mark_point()`|A scatter plot with configurable point shapes|
|rect|`mark_rect()`|A filled rectangle, used for heatmaps|
|rule|`mark_rule()`|A vertical or horizontal line spanning the axis|
|text|`mark_text()`|A scatter plot with points represented by text|
|tick|`mark_tick()`|A vertical or horizontal tick mark|

### Mark Properties
|Property|Type|Description|
|-|-|-|
|opacity|`number`|The overall opacity (value between [0,1]).|
|point|`boolean`|A flag for overlaying points on top of line or area marks, or an object defining the properties of the overlayed points.|

## Data Transofrmations
### Aggregate Transforms
|Operation|Description|
|-|-|
|count|The total count of data objects in the group. |
|valid|The count of field values that are not null, undefined or NaN.|
|missing|The count of null or undefined field values.|
|distinct|The count of distinct field values.|
|sum|The sum of field values.|
|mean|The mean (average) field value.|
|average|The mean (average) field value. Identical to mean.|
|variance|The sample variance of field values.|
|variancep|The population variance of field values.|
|stdev|The sample standard deviation of field values.|
|stdevp|The population standard deviation of field values.|
|stderr|The standard error of field values.|
|median|The median field value.|
|q1|The lower quartile boundary of field values.|
|q3|The upper quartile boundary of field values.|
|ci0|The lower boundary of the bootstrapped 95% confidence interval of the mean field value.|
|ci1|The upper boundary of the bootstrapped 95% confidence interval of the mean field value.|
|min|The minimum field value.|
|max|The maximum field value.|

## Top-Level Chart Configuration
|Property|Type|Description|
|-|-|-|
|height|`number`|The default height of the single plot or each plot in a trellis plot when the visualization has a continuous (non-ordinal) y-scale with `rangeStep` = `null`.|
|width|`number`|The default width of the single plot or each plot in a trellis plot when the visualization has a continuous (non-ordinal) x-scale or ordinal x-scale with `rangeStep` = `null`.|
