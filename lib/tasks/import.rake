require 'csv'

namespace :app do
  desc "Import internships from csv file"
  
  task :import, [:file, :limit] => [:environment] do |t,args|
    args.with_defaults(limit: -1)
    file = args[:file]
    limit = args[:limit]
    
    Internship.delete_all
    
    CSV.foreach(file, :headers => true) do |row, i|
      #Data are this way: Automne 2015 => 2015A. We are separating year and semester
      semester = row[7].split('').last
      semester_year = row[7][0..-1]
  
      Internship.create({
        id: row[0],
        address: row[1],
        branch: row[2],
        company: row[3],
        description: row[4],
        student: row[5],
        level: row[6],
        semester: semester,
        year: semester_year,
        subject: row[8],
        teacher: row[9]
      })
      
      if i == limit
        break
      end
    end
  end
end
#num,addresse,branche,company,description,etudiant,niveau,semestre,sujet,tuteur