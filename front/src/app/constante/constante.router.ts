import { ModuleWithProviders } from '@angular/core';
import { Route, RouterModule } from '@angular/router';

import { AuthGuard } from '../guards/auth.guard';
import { ConstanteComponent } from './constante.component';

const routes: Route[] = [
    {
        path: '',
        component: ConstanteComponent,
        canActivate: [AuthGuard]
    }
];

export const routing: ModuleWithProviders = RouterModule.forChild(routes);
