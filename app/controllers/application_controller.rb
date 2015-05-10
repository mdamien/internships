class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index]

  before_filter CASClient::Frameworks::Rails::Filter

  def index
    @internship_list = true

    #Retrieving most recent year data from database by default
    @internships = Internship.search(params).order_internships_for_table

    #Internship data values in JSON (countries, cities, companies)
    @internship_data_json = {
        "countries" => SortedSet.new,
        "cities" => SortedSet.new,
        "companies" => SortedSet.new
    }

    @internships.each do |i|
      @internship_data_json["countries"].add(i.country)
      @internship_data_json["cities"].add(i.city)
      @internship_data_json["companies"].add(i.company)
    end
  end
  
  def view
    @internship = Internship.find(params[:id])
  end

  def logout
    CASClient::Frameworks::Rails::Filter.logout(self)
  end

  protected

  #Default search parameters.
  def set_search_query
    @all_semesters = Internship.all_semesters_ordered
    @internship_types = Internship.internship_types
    @all_branches = Internship.all_branches_for_select

    # Adding missing parameters by default
    params[:from_semester] ||= @all_semesters.first()
    params[:to_semester] ||= @all_semesters.first()
    params[:internship_type] ||= @internship_types["Tous"]
    params[:branch] ||= "Toutes"
  end
end