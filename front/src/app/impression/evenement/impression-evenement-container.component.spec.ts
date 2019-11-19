import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImpressionEvenementContainerComponent } from './impression-evenement-container.component';

describe('ImpressionEvenementContainerComponent', () => {
  let component: ImpressionEvenementContainerComponent;
  let fixture: ComponentFixture<ImpressionEvenementContainerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImpressionEvenementContainerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImpressionEvenementContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
