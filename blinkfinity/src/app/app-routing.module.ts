import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { EditProgramComponent } from './edit-program/edit-program.component'
import { HomeScreenComponent } from './home-screen/home-screen.component'
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


const routes: Routes = [
  { path: 'home', component: HomeScreenComponent }, // 'home' does not work
  { path: 'edit-program/:id', component: EditProgramComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // redirect to  the homescreen (not working???)
  { path: '**', redirectTo: '/home', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})


export class AppRoutingModule { }
