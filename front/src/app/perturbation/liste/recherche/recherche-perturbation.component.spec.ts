import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecherchePerturbationComponent } from './recherche-perturbation.component';

describe('RecherchePerturbationComponent', () => {
  let component: RecherchePerturbationComponent;
  let fixture: ComponentFixture<RecherchePerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecherchePerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecherchePerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
