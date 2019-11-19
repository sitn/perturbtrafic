import { HttpClient } from '@angular/common/http';
import { APP_INITIALIZER, Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { IConfig } from '../models/IConfig';

@Injectable()
export class ConfigService {

    private _config: IConfig;

    constructor(private _http: HttpClient) { }
    load() {
        return new Promise((resolve, reject) => {
            this._http.get('./assets/config/config.json').pipe(
                map(res => res)
            ).subscribe((data: IConfig) => {
                this._config = data;
                resolve(true);
            });
        });
    }
    // Is app in the development mode?
    /* isDevmode() {
        return this._env === 'development';
    }*/
    // Gets API route based on the provided key
    getWsPath(): string {
        return this._config['wsPath'];
    }
    // Gets a value of specified property in the configuration file
    get(key: any) {
        return this._config[key];
    }

    getConfig(): IConfig {
        return this._config;
    }

    getFieldsMapping(): any {
        return this._config['evenementPerturbationFieldsMapping'];
    }

    getUrlGuichetCarto(): string {
        return this._config['urlGuichetCarto'];
    }

    getUrlConflits(): string {
        return this._config['urlConflits'];
    }

    getWsSitnBaseUrl(): string {
        return this._config['wsSitnBaseUrl'];
    }
}

export function ConfigFactory(config: ConfigService) {
    return () => config.load();
}

export function init() {
    return {
        provide: APP_INITIALIZER,
        useFactory: ConfigFactory,
        deps: [ConfigService],
        multi: true
    };
}

const ConfigModule = {
    init: init
};

export { ConfigModule };
