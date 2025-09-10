/**
 * This directive modifies the inner HTML of elements so that they
 * can render text supplied in a markdown format.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>, Jade Keegan
 * @copyright 2024
 * @license MIT
 */
import { AfterViewInit, Directive, ElementRef } from '@angular/core';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

@Directive({
    selector: '[markdown]',
    standalone: false
})
export class MarkdownDirective implements AfterViewInit {
  constructor(private el: ElementRef) {}

  /**
   * Generates HTML from markdown after the view is initialized.
   * This is needed so that dynamic data is added to the DOM before
   * the markdownify() method is run.
   */
  ngAfterViewInit(): void {
    this.markdownify();
  }

  markdownify() {
    this.el.nativeElement.innerHTML = DOMPurify.sanitize(
      marked.parse(this.el.nativeElement.innerHTML) as string
    );
  }
}
