import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, throwError } from 'rxjs';
import { catchError, finalize, map } from 'rxjs/operators';

import { LoaderService } from './loader/loader.service';
import { UserService } from '../services/user.service';

@Injectable()
export class HttpPendingInterceptor implements HttpInterceptor {
    private _pendingRequests = 0;
    _pendingRequestsStatus: Subject<boolean> = new Subject<boolean>();

    pendingRequestsStatus$ = this._pendingRequestsStatus.asObservable();

    constructor(private loaderService: LoaderService) { }

    get pendingRequests(): number {
        return this._pendingRequests;
    }

    incrementPendingRequests(): void {

    }

    decrementPendingRequests(): void {
        this._pendingRequests--;
    }

    private shouldHideLoader(req: HttpRequest<any>): boolean {
        return req.headers.has('hide-loader');
    }

    interceptRoutingStart(): void {
        this._pendingRequests++;
        if (1 === this._pendingRequests) {

            this.loaderService.show();
        }
    }

    interceptRoutingStop(): void {
        this._pendingRequests--;
        if (0 === this._pendingRequests) {
            this.loaderService.hide();
        }
    }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const shouldHideLoader = this.shouldHideLoader(req);

        if (!shouldHideLoader) {

            this._pendingRequests++;

            if (1 === this._pendingRequests) {

                this.loaderService.show();
            }
        }

        return next.handle(req).pipe(
            map(event => {
                /* if (this.userService.currentUser && this.userService.currentUser.currentEntity
                    && this.userService.currentUser.currentEntity.id) {
                    req.params.append('idEntite', this.userService.currentUser.currentEntity.id.toString());
                } */
                return event;
            }),
            catchError(error => {
                return throwError(error);
            }),
            finalize(() => {
                if (!shouldHideLoader) {
                    this._pendingRequests--;
                    if (0 === this._pendingRequests) {
                        this.loaderService.hide();
                    }
                }
            })
        );
    }
}
