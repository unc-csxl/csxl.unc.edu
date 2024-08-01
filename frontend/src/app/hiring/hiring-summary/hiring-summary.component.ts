import {
  Component,
  computed,
  effect,
  signal,
  WritableSignal
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Term } from 'src/app/academics/academics.models';
import {
  currentTermResolver,
  termsResolver
} from 'src/app/academics/academics.resolver';
import { HiringService } from '../hiring.service';
import { AcademicsService } from 'src/app/academics/academics.service';

@Component({
  selector: 'app-hiring-summary',
  templateUrl: './hiring-summary.component.html',
  styleUrl: './hiring-summary.component.css'
})
export class HiringSummaryComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'summary',
    title: 'Hiring Summary',
    component: HiringSummaryComponent,
    resolve: {
      terms: termsResolver,
      currentTerm: currentTermResolver
    }
  };

  /** Store list of Terms  */
  public terms: Term[];
  public selectedTermId: WritableSignal<string | undefined> = signal(undefined);

  public selectedTerm = computed(() => {
    return this.terms.find((term) => term.id === this.selectedTermId())!;
  });

  /** Effect that updates the hiring data when the selected term changes. */
  selectedTermEffect = effect(() => {
    if (this.selectedTermId()) {
      const term = this.terms.find(
        (term) => term.id === this.selectedTermId()
      )!;
      this.hiringService
        .getHiringAdminOverview(term.id)
        .subscribe((overview) => {
          //this.hiringAdminOverview.set(overview);
        });
    }
  });

  /** Constructor */
  constructor(
    private route: ActivatedRoute,
    protected hiringService: HiringService,
    protected academicsService: AcademicsService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      terms: Term[];
      currentTerm: Term | undefined;
    };

    this.terms = data.terms;
    this.selectedTermId.set(data.currentTerm?.id ?? undefined);
  }
}
