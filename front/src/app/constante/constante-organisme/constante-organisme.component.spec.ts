import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteOrganismeComponent } from './constante-organisme.component';

describe('ConstanteOrganismeComponent', () => {
  let component: ConstanteOrganismeComponent;
  let fixture: ComponentFixture<ConstanteOrganismeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteOrganismeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteOrganismeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
