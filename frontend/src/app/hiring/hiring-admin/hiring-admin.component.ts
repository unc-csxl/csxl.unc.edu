/**
 * Enables the root user to make hiring decisions.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import {
  Component,
  computed,
  effect,
  signal,
  WritableSignal
} from '@angular/core';
import { PublicProfile } from 'src/app/profile/profile.service';
import {
  HiringAdminOverview,
  HiringAssignmentOverview
} from '../hiring.models';
import { HiringService } from '../hiring.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import {
  currentTermResolver,
  termsResolver
} from 'src/app/academics/academics.resolver';
import { ActivatedRoute } from '@angular/router';
import { Term } from 'src/app/academics/academics.models';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-hiring-admin',
  templateUrl: './hiring-admin.component.html',
  styleUrl: './hiring-admin.component.css',
  animations: [
    trigger('detailExpand', [
      state('collapsed,void', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      )
    ])
  ]
})
export class HiringAdminComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'admin',
    title: 'Hiring Administration',
    component: HiringAdminComponent,
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

  /** Store the hiring data. */
  hiringAdminOverview: WritableSignal<HiringAdminOverview | undefined> =
    signal(undefined);

  /** Store the columns to display in the table */
  public displayedColumns: string[] = ['sections', 'instructor', 'totals'];
  /** Store the columns to display when extended */
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  /** Store the element where the dropdown is currently active */
  public expandedElement: HiringAssignmentOverview | null = null;

  /** Effect that updates the hiring data when the selected term changes. */
  selectedTermEffect = effect(() => {
    if (this.selectedTermId()) {
      const term = this.terms.find(
        (term) => term.id === this.selectedTermId()
      )!;
      this.hiringService
        .getHiringAdminOverview(term.id)
        .subscribe((overview) => {
          this.hiringAdminOverview.set(overview);
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

// export const SAMPLE_HIRING_DATA: HiringAdminOverview = {
//   sites: [
//     {
//       sections: ['COMP 110'],
//       instructor: {
//         id: 0,
//         onyen: 'krisj',
//         first_name: 'Kris',
//         last_name: 'Jordan',
//         pronouns: 'he / him',
//         email: 'kris@cs.unc.edu',
//         github_avatar: 'https://avatars.githubusercontent.com/u/31329?v=4',
//         github: null,
//         bio: null,
//         linkedin: null,
//         website: null
//       },
//       coverage: 0,
//       assignments: [
//         {
//           user: {
//             id: 1,
//             onyen: 'atoney',
//             first_name: 'Audrey',
//             last_name: 'Toney',
//             pronouns: 'she / her',
//             email: 'audrey@cs.unc.edu',
//             github_avatar:
//               'https://avatars.githubusercontent.com/u/31745478?v=4',
//             github: null,
//             bio: null,
//             linkedin: null,
//             website: null
//           },
//           level: 'UTA ($2000)',
//           position_number: '1560PA',
//           epar: '201927393',
//           status: 'final'
//         },
//         {
//           user: {
//             id: 0,
//             onyen: 'agandech',
//             first_name: 'Ajay',
//             last_name: 'Gandecha',
//             pronouns: 'he / him',
//             email: 'ajay@cs.unc.edu',
//             github_avatar:
//               'https://avatars.githubusercontent.com/u/17516747?v=4',
//             github: null,
//             bio: null,
//             linkedin: null,
//             website: null
//           },
//           level: 'Lead UTA ($3000)',
//           position_number: '1660WE',
//           epar: '201929083',
//           status: 'draft'
//         },
//         {
//           user: {
//             id: 0,
//             onyen: 'jkeegan',
//             first_name: 'Jade',
//             last_name: 'Keegan',
//             pronouns: 'she / her',
//             email: 'jade@cs.unc.edu',
//             github_avatar:
//               'https://avatars.githubusercontent.com/u/97476936?v=4',
//             github: null,
//             bio: null,
//             linkedin: null,
//             website: null
//           },
//           level: 'Half Load UTA ($1000)',
//           position_number: '2213FQ',
//           epar: '398375265',
//           status: 'commit'
//         }
//       ],
//       preferences: [
//         {
//           id: 0,
//           onyen: 'agandech',
//           first_name: 'Ajay',
//           last_name: 'Gandecha',
//           pronouns: 'he / him',
//           email: 'ajay@cs.unc.edu',
//           github_avatar: 'https://avatars.githubusercontent.com/u/17516747?v=4',
//           github: null,
//           bio: null,
//           linkedin: null,
//           website: null
//         },
//         {
//           id: 1,
//           onyen: 'atoney',
//           first_name: 'Audrey',
//           last_name: 'Toney',
//           pronouns: 'she / her',
//           email: 'audrey@cs.unc.edu',
//           github_avatar: 'https://avatars.githubusercontent.com/u/31745478?v=4',
//           github: null,
//           bio: null,
//           linkedin: null,
//           website: null
//         }
//       ]
//     },
//     {
//       sections: ['COMP 590'],
//       instructor: {
//         id: 1,
//         onyen: 'krisj',
//         first_name: 'Kris',
//         last_name: 'Jordan',
//         pronouns: 'he / him',
//         email: 'kris@cs.unc.edu',
//         github_avatar: 'https://avatars.githubusercontent.com/u/31329?v=4',
//         github: null,
//         bio: null,
//         linkedin: null,
//         website: null
//       },
//       coverage: 0,
//       assignments: [
//         {
//           user: {
//             id: 0,
//             onyen: 'agandech',
//             first_name: 'Ajay',
//             last_name: 'Gandecha',
//             pronouns: 'he / him',
//             email: 'ajay@cs.unc.edu',
//             github_avatar:
//               'https://avatars.githubusercontent.com/u/17516747?v=4',
//             github: null,
//             bio: null,
//             linkedin: null,
//             website: null
//           },
//           level: 'Lead UTA ($3000)',
//           position_number: '1660IIC',
//           epar: '294576032',
//           status: 'commit'
//         }
//       ],
//       preferences: [
//         {
//           id: 0,
//           onyen: 'agandech',
//           first_name: 'Ajay',
//           last_name: 'Gandecha',
//           pronouns: 'he / him',
//           email: 'ajay@cs.unc.edu',
//           github_avatar: 'https://avatars.githubusercontent.com/u/17516747?v=4',
//           github: null,
//           bio: null,
//           linkedin: null,
//           website: null
//         },
//         {
//           id: 0,
//           onyen: 'jkeegan',
//           first_name: 'Jade',
//           last_name: 'Keegan',
//           pronouns: 'she / her',
//           email: 'jade@cs.unc.edu',
//           github_avatar: 'https://avatars.githubusercontent.com/u/97476936?v=4',
//           github: null,
//           bio: null,
//           linkedin: null,
//           website: null
//         }
//       ]
//     }
//   ]
// };
