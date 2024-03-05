import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AmbassadorHomeRoutingModule } from './ambassador-home-routing.module';
import { AmbassadorXlListComponent } from './ambassador-xl/list/ambassador-xl-list.component';
import { MatCard, MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatTabsModule } from '@angular/material/tabs';

@NgModule({
  declarations: [AmbassadorXlListComponent],
  imports: [
    CommonModule,
    AmbassadorHomeRoutingModule,
    MatCardModule,
    MatTabsModule,
    MatTableModule,
    MatDialogModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatListModule,
    MatAutocompleteModule
  ]
})
export class AmbassadorHomeModule {}
