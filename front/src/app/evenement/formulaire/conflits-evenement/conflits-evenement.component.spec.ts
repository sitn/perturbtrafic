import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConflitsEvenementComponent } from './conflits-evenement.component';

describe('ConflitsEvenementComponent', () => {
  let component: ConflitsEvenementComponent;
  let fixture: ComponentFixture<ConflitsEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConflitsEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConflitsEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
