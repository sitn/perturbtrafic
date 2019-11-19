import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConflitComponent } from './conflit.component';

describe('ConflitComponent', () => {
  let component: ConflitComponent;
  let fixture: ComponentFixture<ConflitComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConflitComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConflitComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
