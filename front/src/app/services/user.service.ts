import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { catchError, map, mergeMap, flatMap, switchMap } from 'rxjs/operators';

import { IAutorisations } from '../models/IAutorisations';
import { IUser } from '../models/IUser';
import { ApiService } from './api.service';
import { CookieService } from './cookie.service';
import { Router } from '@angular/router';

@Injectable({
    providedIn: 'root'
})
export class UserService {

    currentUser: IUser;

    private userSubject = new Subject<IUser>();

    userState = this.userSubject.asObservable();

    constructor(private cookieService: CookieService, private apiService: ApiService, private router: Router) {
    }

    setUser(user: IUser) {
        this.currentUser = user;
        this.userSubject.next(user);
    }


    setAutorisations(autorisations: IAutorisations): void {
        this.currentUser.autorisations = autorisations;
        this.userSubject.next(this.currentUser);
    }

    isLoggedUser(): Observable<boolean> {
        return this.retrieveAndSetLoggedUser().pipe(
            switchMap((user: IUser) => {
                return this.getUserAutorisations().pipe(
                    map((autorisations: IAutorisations) => {
                        this.setAutorisations(autorisations);
                        return true;
                    }),
                    catchError((error: any) => {
                        return of(false);
                    })
                );
            })
        );
    }


    retrieveAndSetLoggedUser(): Observable<IUser> {
        return this.apiService.getLoggedUser().pipe(
            map((user: IUser) => {
                if (user.entites && this.cookieService.get('idEntity')) {
                    const entity = user.entites.find(ent => {
                        return ent.id.toString() === this.cookieService.get('idEntity');
                    });
                    if (entity) {
                        user.currentEntity = entity;
                    }
                } else if (user && user.entites && user.entites.length > 0) {
                    user.currentEntity = user.entites[0];
                }
                this.setUser(user);
                return user;
            }),
            catchError((error: any) => {
                this.setUser(null);
                return null as Observable<IUser>;
            })
        );
    }

    getUserAutorisations(): Observable<IAutorisations> {
        return this.apiService.getUserAutorisations().pipe(
            map((autorisations: IAutorisations) => {
                return autorisations;
            }),
            catchError((error: any) => {
                this.setUser(null);
                return null as Observable<IAutorisations>;
            })
        );
    }

    setCurrentEntity(entity) {
        this.cookieService.set('idEntity', entity.id.toString());
        this.currentUser.currentEntity = entity;
        this.userSubject.next(this.currentUser);
    }

    removeUser() {
        this.cookieService.remove('auth_tkt');
        this.currentUser = null;
        this.userSubject.next(null);
    }

    canAddEvent() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.ajouter_evenement;
    }

    canAddPerturbation() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.ajouter_perturbation;
    }

    canEditPerturbationState() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.modifier_etat_perturbation_creation;
    }

    canManageContact() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.gerer_contacts;
    }

    canManageOrganisme() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.gerer_organismes;
    }

    canManagePreavis() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.gerer_contacts_preavis;
    }

    canManageAvisUrgence() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.gerer_contacts_avis_urgences;
    }

    canManageSrb() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.gerer_contacts_srb;
    }

    canManageDelegation() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.peut_deleguer;
    }

    canManageUtilisateurs() {
        return this.currentUser && this.currentUser.autorisations && this.currentUser.autorisations.gerer_utilisateurs;
    }

}
