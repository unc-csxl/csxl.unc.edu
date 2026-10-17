import {
  Component,
  DestroyRef,
  ElementRef,
  TemplateRef,
  ViewChild,
  computed,
  signal
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Title } from '@angular/platform-browser';
import { Router, TitleStrategy } from '@angular/router';
import { NavigationService } from '../../../navigation/navigation.service';
import {
  Subject,
  catchError,
  finalize,
  fromEvent,
  map,
  merge,
  of,
  switchMap,
  timer
} from 'rxjs';
import { OperatingHours } from '../../coworking.models';
import {
  OperatingHoursService,
  operatingHoursError
} from '../../operating-hours.service';
import {
  operatingHoursDate,
  operatingHoursInput,
  operatingHoursTime
} from '../../operating-hours-time';
import { OperatingHoursEditorDialog } from '../../widgets/operating-hours-editor/operating-hours-editor.dialog';
import { PermissionService } from '../../../permission.service';

/** Manage the coworking schedule within the ambassador view. */
@Component({
  selector: 'app-ambassador-hours',
  templateUrl: './ambassador-hours.component.html',
  standalone: false
})
export class AmbassadorHoursComponent {
  private readonly refresh = new Subject<void>();
  private readonly hours = signal<OperatingHours[]>([]);
  private readonly now = signal(Date.now());
  private requestedEnd = this.nextMonth(new Date());
  loadedEnd = signal<Date | null>(null);
  loading = signal(false);
  error = signal('');
  deletingId = signal<number | null>(null);
  activeHours = computed(() =>
    this.hours().filter(
      (hours) =>
        hours.start.getTime() <= this.now() && hours.end.getTime() > this.now()
    )
  );
  futureHours = computed(() =>
    this.hours().filter((hours) => hours.start.getTime() > this.now())
  );
  formatDate = operatingHoursDate;
  formatTime = operatingHoursTime;

  @ViewChild('confirmDelete') confirmDelete!: TemplateRef<{
    $implicit: OperatingHours;
  }>;
  @ViewChild('addHoursButton', { read: ElementRef })
  addHoursButton?: ElementRef<HTMLButtonElement>;

  constructor(
    private service: OperatingHoursService,
    private permission: PermissionService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    destroyRef: DestroyRef,
    navigation: NavigationService,
    title: Title,
    router: Router,
    titleStrategy: TitleStrategy
  ) {
    navigation.setTitle('Operating Hours');
    title.setTitle(
      'Operating Hours | CS Experience Labs | CSXL at UNC-Chapel Hill'
    );
    destroyRef.onDestroy(() =>
      titleStrategy.updateTitle(router.routerState.snapshot)
    );
    timer(0, 1000)
      .pipe(takeUntilDestroyed(destroyRef))
      .subscribe(() => this.now.set(Date.now()));
    merge(
      timer(0, 30000),
      fromEvent(window, 'focus'),
      this.refresh,
      service.changes$
    )
      .pipe(
        switchMap(() => {
          if (!this.permission.checkSignal('coworking.reservation.*', '*'))
            return of(null);
          this.loading.set(true);
          const end = this.requestedEnd;
          return this.service
            .list(`${operatingHoursInput(new Date()).slice(0, 10)}T00:00`, end)
            .pipe(
              catchError(() => {
                this.error.set(
                  'Unable to load operating hours. Please try again.'
                );
                return of(null);
              }),
              finalize(() => this.loading.set(false))
            )
            .pipe(map((hours) => (hours ? { hours, end } : null)));
        }),
        takeUntilDestroyed(destroyRef)
      )
      .subscribe((result) => {
        if (result) {
          const unique = new Map(
            result.hours.map((hours) => [hours.id, hours])
          );
          this.hours.set(
            [...unique.values()].sort(
              (a, b) => a.start.getTime() - b.start.getTime()
            )
          );
          this.loadedEnd.set(result.end);
          this.error.set('');
        }
      });
  }

  canCreate(): boolean {
    return this.permission.checkSignal(
      'coworking.operating_hours.create',
      'coworking/operating_hours'
    );
  }

  retry(): void {
    this.refresh.next();
  }

  loadMore(): void {
    if (this.loading()) return;
    this.requestedEnd = this.nextMonth(this.loadedEnd() ?? this.requestedEnd);
    this.refresh.next();
  }

  edit(hours?: OperatingHours): void {
    const action = hours ? 'update' : 'create';
    const resource =
      'coworking/operating_hours' + (hours ? `/${hours.id}` : '');
    if (
      !this.permission.checkSignal(
        `coworking.operating_hours.${action}`,
        resource
      )
    )
      return;
    this.dialog.open(OperatingHoursEditorDialog, {
      width: '640px',
      maxWidth: '95vw',
      data: { hours, schedule: this.hours() }
    });
  }

  delete(hours: OperatingHours): void {
    if (
      this.deletingId() !== null ||
      !this.permission.checkSignal(
        'coworking.operating_hours.delete',
        `coworking/operating_hours/${hours.id}`
      )
    )
      return;
    this.dialog
      .open(this.confirmDelete, {
        data: hours,
        width: '440px',
        maxWidth: '95vw',
        autoFocus: '[data-cancel]'
      })
      .afterClosed()
      .subscribe((confirmed) => {
        if (!confirmed) return;
        const current = this.hours().find((item) => item.id === hours.id);
        if (!current || current.start.getTime() <= Date.now()) {
          this.snackBar.open(
            'Only future hours can be deleted. The schedule has changed.',
            'Dismiss',
            { duration: 6000 }
          );
          this.retry();
          return;
        }
        this.deletingId.set(hours.id);
        this.service
          .delete(hours.id)
          .pipe(finalize(() => this.deletingId.set(null)))
          .subscribe({
            next: () => {
              this.snackBar.open('Operating hours deleted.', 'Dismiss', {
                duration: 4000
              });
              this.addHoursButton?.nativeElement.focus();
            },
            error: (error) => {
              this.snackBar.open(operatingHoursError(error), 'Dismiss', {
                duration: 6000
              });
              this.retry();
            }
          });
      });
  }

  private nextMonth(date: Date): Date {
    const next = new Date(date);
    next.setDate(next.getDate() + 30);
    return next;
  }
}
