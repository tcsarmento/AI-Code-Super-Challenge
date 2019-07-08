import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaLogComponent } from './lista-log.component';

describe('ListaLogComponent', () => {
  let component: ListaLogComponent;
  let fixture: ComponentFixture<ListaLogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ListaLogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListaLogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
