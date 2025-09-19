import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
    selector: 'search-bar',
    templateUrl: './search-bar.widget.html',
    styleUrls: ['./search-bar.widget.css'],
    standalone: false
})
export class SearchBar {
  @Input() searchBarQuery: string = '';
  @Output() searchBarQueryChange = new EventEmitter<string>();

  constructor() {}

  onTextChanged() {
    this.searchBarQueryChange.emit(this.searchBarQuery);
  }
  clearSearch() {
    this.searchBarQuery = '';
    this.searchBarQueryChange.emit(this.searchBarQuery);
  }
}
