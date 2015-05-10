class Internship < ActiveRecord::Base
  include Filterable

  scope :from_year, -> (year) { where("year >= ?", year) }
  scope :to_year, -> (year) { where("year <= ?", year) }
  scope :from_semester, -> (from_year, from_semester) { where.not("semester LIKE '%P%' and year = ?", from_year) unless from_semester == 'P' }
  scope :to_semester, -> (to_year, to_semester) { where.not("semester LIKE '%A%' and year = ?", to_year) unless to_semester == 'A' }
  scope :company_like, -> (company) { where("company LIKE ?", "%"+ company + "%") }
  scope :country_like, -> (country) { where("country LIKE ?", "%"+ country + "%") }
  scope :city_like, -> (city) { where("city LIKE ?", "%"+ city + "%") }
  scope :filiere_like, -> (filiere) { where("filiere LIKE ?", "%"+ filiere + "%") }
  scope :branch_like, -> (branch) { where("branch LIKE ?", "%"+ branch + "%") }
  scope :confidential_only, -> { where("confidential = 't'") }
  scope :exclude_not_done, -> { where("done = 't'") }

  scope :order_by_semester_desc, -> { order(year: :DESC).order(semester: :ASC) }
  scope :order_by_semester_asc, -> { order(year: :ASC).order(semester: :DESC) }

  def self.order_internships_for_table
    return order(year: :DESC)
           .order(semester: :ASC)
           .order(country: :ASC)
           .order(company: :ASC)
  end

  def self.most_recent_internships
    most_recent_year = Internship.maximum("year")
    return Internship.from_year(most_recent_year)
  end

  def self.search query
    if query.has_key?(:from_semester) && query.has_key?(:to_semester) && query.has_key?(:internship_type) && query.has_key?(:branch)

      from_year = query[:from_semester][1..4].to_i
      to_year = query[:to_semester][1..4].to_i
      from_semester = query[:from_semester][0]
      to_semester = query[:to_semester][0]

      internships = from_year(from_year)
                        .to_year(to_year)
                        .from_semester(from_year, from_semester)
                        .to_semester(to_year, to_semester)

      case query[:internship_type]
        when "tn05"
          internships = internships.where("level LIKE '%ouvrier%'")
        when "tn09"
         internships = internships.where("level LIKE '%assistant%'")
        when "tn10"
          internships = internships.where("level LIKE '%projet de fin%'")
        when "intercultural"
          internships = internships.where("level LIKE '%interculturel%'")
        when "apprenticeship"
          internships = internships.where("level LIKE '%apprentissage%'")
      end

      # Branch filter if internship type is not tn05 or not all internships.
      if (query[:internship_type] != "tn05" || query[:internship_type] != "all") && query[:branch] != "Toutes"
        internships = internships.branch_like(query[:branch])
      end

      return internships
    end

    # Returning most recent internships if missing parameters.
    return most_recent_internships
  end

  def self.internship_count_by_semester query
    internships = search(query)

    internships = internships.filter(query.slice(:company_like, :country_like, :city_like, :filiere_like, :done_only))
    internships = internships.confidential_only if query[:confidential_only].present?
    internships = internships.exclude_not_done unless query[:include_not_done].present?
    internships = internships
                      .group("year")
                      .group("semester")
                      .group("branch")
                      .order_by_semester_asc
                      .count

    return internships
  end

  def self.all_internship_years
    return select(:year).distinct.order(year: :ASC)
  end

  def self.all_branches
    return select(:branch).distinct.order(branch: :ASC)
  end

  def self.all_branches_for_select
    branches = self.all_branches.map { |b| b.branch }
    branches.unshift("Toutes")

    return branches
  end

  def self.internship_types
    return {
        "Tous" => "all",
        "TN05" => "tn05",
        "TN09" => "tn09",
        "TN10" => "tn10",
        "Apprentissage" => "apprenticeship",
        "Interculturel" => "intercultural"
    }
  end

  def self.all_semesters_ordered
    semesters_in_database = select(:year).select(:semester).distinct.group("year").group("semester").order_by_semester_desc

    # Semesters will be sorted already, as we already sorted the data from the database.
    semesters = Array.new

    semesters_in_database.each do |s|
      semesters.push(s.semester + s.year.to_s)
    end

    return semesters
  end

  def self.all_countries_ordered_for_select
    return  select(:country).distinct.order(country: :ASC).map { |c| c.country }
  end

end