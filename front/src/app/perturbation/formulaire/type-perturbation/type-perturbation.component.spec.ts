import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TypePerturbationComponent } from './type-perturbation.component';

describe('TypePerturbationComponent', () => {
  let component: TypePerturbationComponent;
  let fixture: ComponentFixture<TypePerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TypePerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TypePerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
