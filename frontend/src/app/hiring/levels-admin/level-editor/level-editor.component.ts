import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HiringLevel, HiringLevelClassification } from '../../hiring.models';
import { HiringService } from '../../hiring.service';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'app-level-editor',
    templateUrl: './level-editor.component.html',
    styleUrl: './level-editor.component.css',
    standalone: false
})
export class LevelEditorComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'levels/:id/edit',
    title: 'Hiring Level Editor',
    component: LevelEditorComponent
  };

  classification = HiringLevelClassification;

  /** Stores the ID from the route */
  id: string;

  /** Stores the level being edited */
  level: HiringLevel;

  /** Level Form */
  public levelForm = this.formBuilder.group({
    title: new FormControl('', [Validators.required]),
    salary: new FormControl(0.0, [Validators.required]),
    load: new FormControl(0.0, [Validators.required]),
    classification: new FormControl(HiringLevelClassification.UG, [
      Validators.required
    ]),
    is_active: new FormControl(true, [Validators.required])
  });

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected hiringService: HiringService,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar
  ) {
    // Find the ID from the route
    this.id = route.snapshot.params['id'];
    // Initialize the level data
    if (this.id === 'new') {
      this.level = {
        id: null,
        title: '',
        salary: 0.0,
        load: 1.0,
        classification: HiringLevelClassification.UG,
        is_active: true
      };
    } else {
      this.level = this.hiringService.getHiringLevel(+this.id)!;
    }
    // Set the form data
    this.levelForm.patchValue(this.level);
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.levelForm.valid) {
      let levelToSubmit = this.level;
      Object.assign(levelToSubmit, this.levelForm.value);

      let submittedLevel = this.isNew()
        ? this.hiringService.createHiringLevel(levelToSubmit)
        : this.hiringService.updateHiringLevel(levelToSubmit);

      submittedLevel.subscribe({
        next: (_) => {
          this.router.navigate(['/hiring/levels']);
          this.snackBar.open(`Level ${this.action()}`, '', {
            duration: 2000
          });
        },
        error: (_) => {
          this.snackBar.open(`Error: Level Not ${this.action()}`, '', {
            duration: 2000
          });
        }
      });
    }
  }

  /** Event handler to handle resetting the form.
   * @returns {void}
   */
  onReset() {
    this.levelForm.patchValue(this.level);
  }

  /** Shorthands for whether a level is new or not.
   * @returns {boolean}
   */
  isNew(): boolean {
    return this.route.snapshot.params['id'] === 'new';
  }
  action(): string {
    return this.isNew() ? 'Created' : 'Updated';
  }
}
