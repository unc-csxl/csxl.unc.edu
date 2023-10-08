import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { map } from 'rxjs/operators';
import { Organization } from '../../organization.service';
import { Profile } from 'src/app/profile/profile.service';
import { PermissionService } from 'src/app/permission.service';
import { Observable } from 'rxjs';

@Component({
    selector: 'organization-details-info-card',
    templateUrl: './organization-details-info-card.widget.html',
    styleUrls: ['./organization-details-info-card.widget.css']
})
export class OrganizationDetailsInfoCard implements OnInit, OnDestroy {

    @Input() organization?: Organization;
    @Input() profile?: Profile;

    public isHandset: boolean = false;
    private isHandsetSubscription!: Subscription;

    public isTablet: boolean = false;
    private isTabletSubscription!: Subscription;

    /** Stores whether the user has admin permission over the current organization. */
    public adminPermission$: Observable<boolean>;

    constructor(private breakpointObserver: BreakpointObserver, private permission: PermissionService) {
        this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    }

    ngOnInit(): void {
        this.isHandsetSubscription = this.initHandset();
        this.isTabletSubscription = this.initTablet();
    }

    ngOnDestroy(): void {
        this.isHandsetSubscription.unsubscribe();
        this.isTabletSubscription.unsubscribe();
    }

    private initHandset() {
        return this.breakpointObserver
            .observe([Breakpoints.Handset, Breakpoints.TabletPortrait])
            .pipe(map(result => result.matches))
            .subscribe(isHandset => this.isHandset = isHandset);
    }

    private initTablet() {
        return this.breakpointObserver
            .observe(Breakpoints.TabletLandscape)
            .pipe(map(result => result.matches))
            .subscribe(isTablet => this.isTablet = isTablet);
    }

}

