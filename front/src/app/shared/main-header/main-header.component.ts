import { Component, ViewChild, ElementRef, HostListener, OnInit } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { Subscription } from 'rxjs';
import { IUser } from 'src/app/models/IUser';
import { Align, Margin } from '@progress/kendo-angular-popup';
import { ConfigService } from 'src/app/services/config.service';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';
import { version } from '../../../../package.json';

@Component({
    selector: 'main-header',
    templateUrl: './main-header.component.html',
    styleUrls: ['./main-header.component.scss']
})
export class MainHeaderComponent implements OnInit {

    @ViewChild('anchor', { static: false }) public anchor: ElementRef;
    @ViewChild('popup', { read: ElementRef, static: false }) public popup: ElementRef;

    items: any[];
    userEntities: any[];
    show: boolean;
    subscriptions: Subscription[];
    currentUser: IUser;
    anchorAlign: Align;
    popupMargin: Margin;
    popupAlign: any;
    version: string;

    @HostListener('document:click', ['$event'])
    public documentClick(event: any): void {
        if (!this.contains(event.target)) {
            this.toggle(false);
        }
    }

    constructor(private router: Router, private configService: ConfigService, private userService: UserService,
        private apiService: ApiService) {
        this.show = false;
        this.items = [
            {
                text: 'Evénements',
                path: '/evenements',
                cssClass: 'active',
            }, {
                text: 'Perturbations',
                path: '/perturbations',
                cssClass: 'active'
            }, {
                text: 'Conflits',
                path: '/conflits',
                disabled: false
            }, {
                text: 'Données constantes',
                path: '/constantes',
                disabled: false
            }, {
                text: 'Guichet-Carto',
                path: '/guichet-carto',
                newTab: true,
                absoluteUrl: this.configService.getUrlGuichetCarto()
            }, {
                text: 'Mode d\'emploi',
                newTab: true,
                absoluteUrl: '/assets/docs/manuel_perturbtrafic.pdf'
            }
        ];
        this.subscriptions = [];
        this.anchorAlign = { horizontal: 'right', vertical: 'bottom' };
        this.popupAlign = { horizontal: 'center', vertical: 'top' };
        this.popupMargin = { horizontal: -1, vertical: 0 };
    }

    ngOnInit() {

        this.version = this.configService.getConfig().version;
        this.buildMenu();

        this.userEntities = [
            {
                text: 'Nicolas Isabey',
                cssClass: 'active',
                items: [
                    { text: 'Entité 1' },
                    { text: 'Entité 2' },
                    { text: 'Déconnexion' }
                ]
            }
        ];


        this.subscriptions.push(this.userService.userState
            .subscribe((user: IUser) => {
                this.currentUser = user;
                this.buildMenu();
            })
        );
    }

    private contains(target: any): boolean {
        if (this.anchor) {
            return this.anchor.nativeElement.contains(target) ||
                (this.popup ? this.popup.nativeElement.contains(target) : false);
        }
    }

    buildMenu() {
        let evenementSubItems: any[] = [];
        let perturbationSubItems: any[] = [];
        if (this.userService.canAddEvent()) {
            evenementSubItems = [
                { text: 'Evénements', path: '/evenements' },
                { text: 'Nouvel evenement', path: '/evenements/formulaire' }
            ];
        }
        if (this.userService.canAddPerturbation()) {
            perturbationSubItems = [
                { text: 'Perturbations', path: '/perturbations' },
                { text: 'Nouvelle perturbation', path: '/perturbations/formulaire' }
            ];
        }
        this.items = [
            {
                text: 'Evénements',
                cssClass: 'active',
                items: evenementSubItems
            }, {
                text: 'Perturbations',
                cssClass: 'active',
                items: perturbationSubItems
            }, {
                text: 'Conflits',
                path: '/conflits',
                disabled: false
            }, {
                text: 'Données constantes',
                path: '/constantes',
                disabled: false
            }, {
                text: 'Guichet-Carto',
                path: '/guichet-carto',
                newTab: true,
                absoluteUrl: this.configService.getUrlGuichetCarto()
            }, {
                text: 'Mode d\'emploi',
                newTab: true,
                absoluteUrl: '/assets/docs/manuel_perturbtrafic.pdf'
            }
        ];
    }

    updateUserEntity(entity: any) {
        this.userService.setCurrentEntity(entity);
        this.router.navigate(['/evenements']);
    }

    onMenuSelect({ item }): void {
        if (item.absoluteUrl && item.newTab) {
            window.open(item.absoluteUrl, '_blank');
        } else {
            if (item && item.path) {
                this.router.navigate([item.path]);
            }
        }
    }

    logout(): void {
        this.apiService.logout().subscribe(val => {
            this.userService.removeUser();
            this.router.navigate(['/login']);
        });
    }

    public toggle(show?: boolean): void {
        this.show = show !== undefined ? show : !this.show;
    }

}
