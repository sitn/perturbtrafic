import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CartePerturbationComponent } from './carte-perturbation.component';

describe('CartePerturbationComponent', () => {
  let component: CartePerturbationComponent;
  let fixture: ComponentFixture<CartePerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CartePerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CartePerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
