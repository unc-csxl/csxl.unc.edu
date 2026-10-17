import {
  Component,
  DestroyRef,
  Input,
  TemplateRef,
  signal
} from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { filter } from 'rxjs';

export interface TabLink {
  label: string;
  path: string;
  icon: string;
}
@Component({
  selector: 'tab-container',
  templateUrl: './tab-container.widget.html',
  styleUrls: ['./tab-container.widget.css'],
  standalone: false
})
export class TabContainerWidget {
  @Input() links: TabLink[] = [];
  @Input() localTab: { label: string; icon: string } | null = null;
  @Input() localContent: TemplateRef<unknown> | null = null;
  localSelected = signal(false);

  constructor(router: Router, destroyRef: DestroyRef) {
    router.events
      .pipe(
        filter((event) => event instanceof NavigationEnd),
        takeUntilDestroyed(destroyRef)
      )
      .subscribe(() => this.localSelected.set(false));
  }
}
