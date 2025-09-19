/**
 * Custom implementation of a filter chip based off of Material 3
 * standards.
 *
 * @see https://m3.material.io/components/chips/guidelines
 *
 * @author Ajay Gandecha <ajay@cs.unc.edu>
 * @license MIT
 * @copyright 2025
 */

import {
  Component,
  computed,
  input,
  Input,
  model,
  signal
} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatFilterChipDialog } from './dialog/filter-chip-dialog.component';

export type MatFilterChipSearchableItem<SelectItemT> = {
  item: SelectItemT;
  displayText: string;
};

/**
 * Defines a functional type to be used to check whether any filterable item
 * matches the text query. This is generic so that it can be applied to any
 * type of item input.
 *
 * @params item The item to check against the query.
 * @params query The text query to check against the item.
 * @returns boolean Whether or not the item matches the query.
 */
export type MatFilterChipFilterLogic<SelectItemT> = (
  item: MatFilterChipSearchableItem<SelectItemT>,
  query: string
) => boolean;

@Component({
    selector: 'mat-filter-chip',
    templateUrl: './filter-chip.component.html',
    styleUrl: './filter-chip.component.css',
    standalone: false
})
export class MatFilterChipComponent<SelectItemT> {
  // Placeholder text for the filter input when no items are selected.
  placeholder = input<string>('Filter');
  // Leading icon to show when the chip is in the default state
  leadingIcon = input<string | null>(null);
  // Whether or not the dropdown should be left or right aligned.
  dropdownAlignment = input<'left' | 'right'>('left');

  // Two-way binding for the chip's selected items.
  selectedItems = model<MatFilterChipSearchableItem<SelectItemT>[]>([]);
  // Input used for the list of items that can be selected.
  searchableItems = input<MatFilterChipSearchableItem<SelectItemT>[]>([]);

  // Stores the logic for how to apply filters based on the search query
  filterLogic = input<MatFilterChipFilterLogic<SelectItemT>>(() => true);

  // Stores whether or not the dropdown is open.
  dropdownOpen = signal<boolean>(false);
  toggleDropdown = () => this.dropdownOpen.set(!this.dropdownOpen());

  // Determine the display text
  displayText = computed(() => {
    if (this.selectedItems().length === 0) {
      return this.placeholder();
    }
    if ((this, this.selectedItems().length === 1)) {
      return this.selectedItems()[0].displayText;
    } else {
      return `${this.selectedItems()[0].displayText}, +${this.selectedItems().length - 1}`;
    }
  });

  constructor(protected dialog: MatDialog) {}

  openDialog(event: MouseEvent) {
    // Constants to save the height and width of the dialog
    const height = 300;
    const width = 200;
    const borderRadiusOffset = 16;
    const topOffset = 8;
    // Determine the absolute position of the dialog, which should be
    // underneath the filter chip. The alignment option should position
    // the dialog to be aligned with the left or right side of the chip.
    const elementBounds = (
      event.currentTarget as HTMLElement
    ).getBoundingClientRect();
    const topPosition = elementBounds.bottom + topOffset;
    const leftPosition =
      this.dropdownAlignment() === 'left'
        ? elementBounds.left - borderRadiusOffset
        : elementBounds.left - width + borderRadiusOffset;

    const dialogRef = this.dialog.open(MatFilterChipDialog<SelectItemT>, {
      height: height + 'px',
      width: width + 'px',
      position: {
        top: topPosition + 'px',
        left: leftPosition + 'px'
      },
      // Makes the backdrop transparent so that the dialog can be displayed
      // directly over the content. This is standard in M3's use of dialogs
      // in Google Calendar and other projects.
      backdropClass: 'mat-filter-chip-dialog-backdrop'
    });

    // Pass data directly to the component instance.
    dialogRef.componentInstance.searchableItems = this.searchableItems();
    dialogRef.componentInstance.filterLogic = this.filterLogic();
    dialogRef.componentInstance.selectedItems.next(this.selectedItems());
    // Listen for changes in the list of selected items and update accordingly.
    const selectedItemsSubscription =
      dialogRef.componentInstance.selectedItems$.subscribe((items) => {
        this.selectedItems.set(items);
      });
    // Unsubscribe from the selected items subscription when the dialog is closed.
    dialogRef.afterClosed().subscribe(() => {
      selectedItemsSubscription.unsubscribe();
    });
  }

  clearSelections() {
    this.selectedItems.set([]);
  }
}
