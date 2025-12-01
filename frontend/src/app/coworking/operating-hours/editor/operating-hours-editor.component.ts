import { DatePipe } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { permissionGuard } from 'src/app/permission.guard';
import { TimeRange } from 'src/app/time-range';
import { OperatingHoursService } from '../operating-hours.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-operating-hours-editor',
  templateUrl: './operating-hours-editor.component.html',
  styleUrl: './operating-hours-editor.component.css',
  standalone: false
})
export class OperatingHoursEditorComponent {
  public static Route = {
    path: 'operating-hours/new',
    component: OperatingHoursEditorComponent,
    title: 'Operating Hours',
    canActivate: [
      permissionGuard(
        'coworking.operating_hours.*',
        'coworking/operating_hours'
      )
    ]
  };

  public form = this.formBuilder.group({
    date: new FormControl(this.datePipe.transform(new Date(), 'yyyy-MM-dd'), [
      Validators.required
    ]),
    start: new FormControl(
      this.datePipe.transform(
        new Date().setHours(9, 0, 0, 0),
        'yyyy-MM-ddTHH:mm'
      ),
      [Validators.required]
    ),
    end: new FormControl(
      this.datePipe.transform(
        new Date().setHours(18, 0, 0, 0),
        'yyyy-MM-ddTHH:mm'
      ),
      [Validators.required]
    )
  });

  constructor(
    protected formBuilder: FormBuilder,
    private datePipe: DatePipe,
    protected operatingHoursService: OperatingHoursService,
    protected snackBar: MatSnackBar,
    protected router: Router
  ) {}

  onSubmit() {
    const selectedDate = new Date(this.form.value.date!);
    const startTime = new Date(this.form.value.start!);
    const endTime = new Date(this.form.value.end!);

    // Combine the selected date with the start and end times
    const startDateTime = new Date(
      selectedDate.getFullYear(),
      selectedDate.getMonth(),
      selectedDate.getDate(),
      startTime.getHours(),
      startTime.getMinutes()
    );

    const endDateTime = new Date(
      selectedDate.getFullYear(),
      selectedDate.getMonth(),
      selectedDate.getDate(),
      endTime.getHours(),
      endTime.getMinutes()
    );

    const range: TimeRange = {
      start: startDateTime,
      end: endDateTime
    };

    this.operatingHoursService.newOperatingHours(range).subscribe({
      next: () => {
        this.router.navigateByUrl(`/coworking/operating-hours`);
      },
      error: (err) => {
        this.snackBar.open(`${err.error.message}`, '', {
          duration: 2000
        });
      }
    });
  }
}
