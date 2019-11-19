import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'ouiNonPipe' })
export class OuiNonPipe implements PipeTransform {
    transform(value) {
        return value ? 'Oui' : 'Non';
    }
}
