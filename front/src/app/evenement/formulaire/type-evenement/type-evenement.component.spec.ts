import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TypeEvenementComponent } from './type-evenement.component';

describe('TypeEvenementComponent', () => {
  let component: TypeEvenementComponent;
  let fixture: ComponentFixture<TypeEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TypeEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TypeEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
