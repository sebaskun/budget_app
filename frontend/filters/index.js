import Vue from "vue"

var numeral = require("numeral")

// numeral.register('format', 'percentage2', {
//   regexps: {
//       format: /(P)/,
//       unformat: /(P)/
//   },
//   format: function(value, format, roundingFunction) {
//       var space = numeral._.includes(format, ' P') ? ' ' : '',
//           output;

//       value = value;

//       // check for space before %
//       format = format.replace(/\s?\P/, '');

//       output = numeral._.numberToFormat(value, format, roundingFunction);

//       if (numeral._.includes(output, ')')) {
//           output = output.split('');

//           output.splice(-1, 0, space + '%');

//           output = output.join('');
//       } else {
//           output = output + space + '%';
//       }

//       return output;
//   },
//   unformat: function(string) {
//       return numeral._.stringToNumber(string);
//   }
// });

Vue.filter("currency", (str, curr="D", formated='0,0.00') => {
    let symbol = {
        'S': "S/",
        'D': "$"
    }
    return symbol[curr] + " " + numeral(str).format(formated)
})

Vue.filter("decimal", (str, formated='0,0.00') => {
  return numeral(str).format(formated)
})
