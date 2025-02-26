/**
 * Dropdown dialog that appears when filtering in the
 * mat-filter-chip component.
 *
 * @author Ajay Gandecha <ajay@cs.unc.edu>
 * @license MIT
 * @copyright 2025
 */

import { Component, computed, model } from '@angular/core';
import { MatFilterChipSearchableItem } from '../filter-chip.component';
import { ReplaySubject, Subject } from 'rxjs';
import { MatListOption } from '@angular/material/list';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'mat-filter-chip-dialog',
  templateUrl: './filter-chip-dialog.component.html',
  styleUrl: './filter-chip-dialog.component.css'
})
export class MatFilterChipDialog<SelectItemT> {
  // Chip's selected items.
  // The subject stores the selected items and emits the latest value to subscribers.
  // The selectedItems$ observable can be subscribed to for updates.
  selectedItems: Subject<MatFilterChipSearchableItem<SelectItemT>[]> =
    new ReplaySubject(1);
  selectedItems$ = this.selectedItems.asObservable();
  // Input used for the list of items that can be selected.
  searchableItems: MatFilterChipSearchableItem<SelectItemT>[] = [];

  // Store the current search query
  searchQuery = model<string>('');
  // Filter the items based on the search query
  searchResults = computed(() => {
    const query = this.searchQuery().toLowerCase();
    return this.searchableItems.filter((item) =>
      item.displayText.toLowerCase().startsWith(query)
    );
  });

  // Handle the event for when the selected items change.
  onSelectionChange(newItems: MatListOption[]) {
    this.selectedItems.next(newItems.map((item) => item.value));
  }

  // Clears the current search query.
  onQueryClear() {
    this.searchQuery.set('');
  }

  constructor(
    public dialogRef: MatDialogRef<MatFilterChipDialog<SelectItemT>>
  ) {}
}
