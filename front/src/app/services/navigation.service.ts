import { EventEmitter, Injectable } from '@angular/core';

import { IContact } from '../models/IContact';
import { IOrganisme } from '../models/IOrganisme';

@Injectable({
    providedIn: 'root'
})
export class NavigationService {

    public openNewContactDialog$: EventEmitter<any>;
    public onNewContactDialogClosed$: EventEmitter<any>;
    public openNewOrganismeDialog$: EventEmitter<any>;
    public onNewOrganismeDialogClosed$: EventEmitter<any>;
    public openErrorDialog$: EventEmitter<any>;
    public onErrorDialogClosed$: EventEmitter<any>;
    public openWarningDialog$: EventEmitter<any>;
    public onWarningDialogClosed$: EventEmitter<any>;
    public openSaisieReperageDialog$: EventEmitter<any>;
    public onSaisieReperageDialogClosed$: EventEmitter<any>;

    constructor() {
        this.openNewContactDialog$ = new EventEmitter();
        this.onNewContactDialogClosed$ = new EventEmitter();
        this.openNewOrganismeDialog$ = new EventEmitter();
        this.onNewOrganismeDialogClosed$ = new EventEmitter();
        this.openErrorDialog$ = new EventEmitter();
        this.onErrorDialogClosed$ = new EventEmitter();
        this.openWarningDialog$ = new EventEmitter();
        this.onWarningDialogClosed$ = new EventEmitter();
        this.openSaisieReperageDialog$ = new EventEmitter();
        this.onSaisieReperageDialogClosed$ = new EventEmitter();
    }

    openNewContactDialog(mode: string, contact: IContact, dropdownOrigin?: any): void {
        this.openNewContactDialog$.emit({ mode: mode, contact: contact, dropdownOrigin: dropdownOrigin });
    }

    closeNewContactDialog(needUpdate: boolean = false): void {
        this.onNewContactDialogClosed$.emit(needUpdate);
    }

    openNewOrganismeDialog(mode: string, organisme: IOrganisme): void {
        this.openNewOrganismeDialog$.emit({ mode: mode, organisme: organisme });
    }

    closeNewOrganismeDialog(needUpdate: boolean = false): void {
        this.onNewOrganismeDialogClosed$.emit(needUpdate);
    }

    openErrorDialog(message: string, title: string) {
        this.openErrorDialog$.emit({ message: message, title: title });
    }

    closeErrorDialog() {
        this.onErrorDialogClosed$.emit();
    }

    openWarningDialog(message: string) {
        this.openWarningDialog$.emit(message);
    }

    closeWarningDialog() {
        this.onWarningDialogClosed$.emit();
    }

    openSaisieReperageDialog() {
        this.openSaisieReperageDialog$.emit();
    }

    closeSaisieReperageDialog() {
        this.onSaisieReperageDialogClosed$.emit();
    }

}
