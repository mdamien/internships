class CreateInternships < ActiveRecord::Migration
  def change
    create_table :internships do |t|
      t.string :address
      t.string :company
      t.string :branch
      t.text :description
      t.string :student
      t.string :level
      t.string :semester
      t.integer :year
      t.string :teacher
    end
  end
end