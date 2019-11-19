import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteAvisPerturbationComponent } from './constante-avis-perturbation.component';

describe('ConstanteAvisPerturbationComponent', () => {
  let component: ConstanteAvisPerturbationComponent;
  let fixture: ComponentFixture<ConstanteAvisPerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteAvisPerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteAvisPerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
