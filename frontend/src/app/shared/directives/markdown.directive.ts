/**
 * This directive modifies the inner HTML of elements so that they
 * can render text supplied in a markdown format.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>, Jade Keegan
 * @copyright 2024
 * @license MIT
 */
import {
  AfterViewInit,
  Directive,
  ElementRef,
  Input,
  OnChanges
} from '@angular/core';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

@Directive({
  selector: '[markdown]',
  standalone: false
})
export class MarkdownDirective implements AfterViewInit, OnChanges {
  @Input() markdownData?: string;

  constructor(private el: ElementRef) {}

  ngOnChanges(): void {
    if (this.markdownData !== undefined) {
      this.markdownify();
    }
  }

  /**
   * Generates HTML from markdown after the view is initialized.
   * This is needed so that dynamic data is added to the DOM before
   * the markdownify() method is run.
   */
  ngAfterViewInit(): void {
    if (this.markdownData === undefined) {
      this.markdownify();
    }
  }

  markdownify() {
    this.el.nativeElement.innerHTML = DOMPurify.sanitize(
      marked.parse(
        this.markdownData ?? this.el.nativeElement.innerHTML
      ) as string
    );
  }
}
