import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()

export class LoaderService {

    private loaderSubject = new Subject<boolean>();

    loaderState = this.loaderSubject.asObservable();

    httpLoaderShown = false;
    clientLoaderShown = false;

    constructor() {
    }

    show(clientLoader = false) {
        if (!clientLoader) {
            this.httpLoaderShown = true;
        } else {
            this.clientLoaderShown = true;
        }
        this.loaderSubject.next(true);
    }

    hide(clientLoader = false) {
        if (clientLoader) {
            this.clientLoaderShown = false;
            if (!this.httpLoaderShown) {
                this.loaderSubject.next(false);
            }
        } else {
            this.httpLoaderShown = false;
            if (!this.clientLoaderShown) {
                this.loaderSubject.next(false);
            }
        }
    }

}
