import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RemarqueEvenementComponent } from './remarque-evenement.component';

describe('RemarqueEvenementComponent', () => {
  let component: RemarqueEvenementComponent;
  let fixture: ComponentFixture<RemarqueEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RemarqueEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RemarqueEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
