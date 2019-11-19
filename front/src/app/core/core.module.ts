import { CommonModule } from '@angular/common';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgModule } from '@angular/core';

import { HttpPendingInterceptor } from './http-pending-interceptor';
import { LoaderComponent } from './loader/loader.component';
import { LoaderService } from './loader/loader.service';

@NgModule({
    imports: [
        CommonModule
    ],
    exports: [
        LoaderComponent,
    ],
    declarations: [
        LoaderComponent,
    ],
    providers: [
        LoaderService,
        HttpPendingInterceptor,
        {
            provide: HTTP_INTERCEPTORS,
            useClass: HttpPendingInterceptor,
            multi: true
        }
    ]
})

export class CoreModule { }
