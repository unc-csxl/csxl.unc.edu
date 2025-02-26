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

import { Component, input, Input, model, signal } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatFilterChipDialog } from './dialog/filter-chip-dialog.component';

@Component({
  selector: 'mat-filter-chip',
  templateUrl: './filter-chip.component.html',
  styleUrl: './filter-chip.component.css'
})
export class MatFilterChipComponent<SelectItemT> {
  // Leading icon to show when the chip is in the default state
  leadingIcon = input<string | null>(null);
  // Whether or not the dropdown should be left or right aligned.
  dropdownAlignment = input<'left' | 'right'>('left');

  // Two-way binding for the chip's selected items.
  selectedItems = model<SelectItemT[]>([]);
  // Input used for the list of items that can be selected.
  searchableItems = input<SelectItemT[]>([]);

  // Stores whether or not the dropdown is open.
  dropdownOpen = signal<boolean>(false);
  toggleDropdown = () => this.dropdownOpen.set(!this.dropdownOpen());

  // Search query for the search bar in the dialog.
  searchQuery = signal<string>('');

  constructor(protected dialog: MatDialog) {}

  openDialog(event: MouseEvent) {
    // Constants to save the height and width of the dialog
    const height = 300;
    const width = 300;
    const borderRadiusOffset = 16;
    // Determine the absolute position of the dialog, which should be
    // underneath the filter chip. The alignment option should position
    // the dialog to be aligned with the left or right side of the chip.
    const elementBounds = (
      event.currentTarget as HTMLElement
    ).getBoundingClientRect();
    const topPosition = elementBounds.bottom;
    const leftPosition =
      this.dropdownAlignment() === 'left'
        ? elementBounds.left - borderRadiusOffset
        : elementBounds.left - 300 + elementBounds.width + borderRadiusOffset;

    this.dialog.open(MatFilterChipDialog<SelectItemT>, {
      height: height + 'px',
      width: width + 'px',
      position: {
        top: topPosition + 'px',
        left: leftPosition + 'px'
      },
      // Hides the backdrop so that the dialog can be displayed directly
      // over the content. This is standard in M3's use of dialogs
      // in Google Calendar and other projects.
      hasBackdrop: false
    });
  }
}
