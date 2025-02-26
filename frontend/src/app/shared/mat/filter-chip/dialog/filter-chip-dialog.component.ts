/**
 * Dropdown dialog that appears when filtering in the
 * mat-filter-chip component.
 *
 * @author Ajay Gandecha <ajay@cs.unc.edu>
 * @license MIT
 * @copyright 2025
 */

import {
  Component,
  effect,
  EventEmitter,
  input,
  model,
  signal,
  WritableSignal
} from '@angular/core';
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

  // Handle the event for when the selected items change.
  onSelectionChange(newItems: MatListOption[]) {
    this.selectedItems.next(newItems.map((item) => item.value));
  }

  constructor(
    public dialogRef: MatDialogRef<MatFilterChipDialog<SelectItemT>>
  ) {}
}
