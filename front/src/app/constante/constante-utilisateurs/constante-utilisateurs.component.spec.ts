import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteUtilisateursComponent } from './constante-utilisateurs.component';

describe('ConstanteUtilisateursComponent', () => {
  let component: ConstanteUtilisateursComponent;
  let fixture: ComponentFixture<ConstanteUtilisateursComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteUtilisateursComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteUtilisateursComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
