// instantiate the bloodhound suggestion engine
var locations = new Bloodhound({
  datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.num); },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  local: [
    { num: 'Sandy Lane' },
    { num: 'Granville Road' },
    { num: 'three' },
    { num: 'four' },
    { num: 'five' },
    { num: 'six' },
    { num: 'seven' },
    { num: 'eight' },
    { num: 'nine' },
    { num: 'ten' }
  ]
});
 
// initialize the bloodhound suggestion engine
locations.initialize();
 
// instantiate the typeahead UI
$('road').typeahead(null, {
  displayKey: 'num',
  source: locations.ttAdapter()
});