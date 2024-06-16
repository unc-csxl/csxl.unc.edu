import { Component, Input } from '@angular/core';

export interface TabLink {
  label: string;
  path: string;
  icon: string;
}
@Component({
  selector: 'tab-container',
  templateUrl: './tab-container.widget.html',
  styleUrls: ['./tab-container.widget.css']
})
export class TabContainerWidget {
  @Input() links: TabLink[] = [];
}
