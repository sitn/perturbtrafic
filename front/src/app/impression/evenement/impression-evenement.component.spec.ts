import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImpressionEvenementComponent } from './impression-evenement.component';

describe('ImpressionEvenementComponent', () => {
  let component: ImpressionEvenementComponent;
  let fixture: ComponentFixture<ImpressionEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImpressionEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImpressionEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
